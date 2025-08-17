import pygame
import math
from random import randint, randrange, choice

pygame.init()

width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GAME")

clock = pygame.time.Clock()

player_img = pygame.transform.scale(pygame.image.load("Images/player.png"), (48, 48)).convert_alpha()
background_img = pygame.transform.scale(pygame.image.load("Images/bg3.png"), (2500, 2250)).convert_alpha()
obstacle_img = pygame.transform.scale(pygame.image.load("Images/obstacle.png"), (64, 64)).convert_alpha()
orb_img = pygame.image.load("Images/phase_orb.png").convert_alpha()
vert_img = pygame.image.load("Images/vert_wall.png").convert_alpha()
hor_img = pygame.image.load("Images/hor_wall.png").convert_alpha()
anim_vert = pygame.image.load("Images/anim_test.png").convert_alpha()



def move_environment(environment: list, direction: str):
    for object in environment:
        object.move(direction)

def random_coords():
    return randint(-200, 1100)

class Player:
    def __init__(self, x, y, default_speed, image):
        self.x = x
        self.y = y
        self.default_speed = default_speed
        self.image = image
        self.velocity = self.default_speed
        self.diag_vel = math.sqrt(self.velocity**2/2)
        self.mv_up = False
        self.mv_down = False
        self.mv_right = False
        self.mv_left = False
        self.rect = image.get_rect()
        self.colliding = False
        self.phase_count = 0
        self.phase_key = False
        


    def move(self):
        if self.check_diagonal():
            self.velocity = self.diag_vel
        if self.mv_up:
            if not self.check_collision("up"):
                if self.y >= 320:
                    self.y -= self.velocity
                elif background.y <= 0:
                    move_environment(all_environment, "up")
                elif self.y - self.velocity > 0:
                    self.y -= self.velocity
            else:
                self.phase("up")

        elif self.mv_down:
            if not self.check_collision("down"):
                if self.y <= 380:
                    self.y += self.velocity
                elif background.y + background_img.get_height() > height:
                    move_environment(all_environment, "down")
                elif self.y + self.velocity + player_img.get_height() < height:
                    self.y += self.velocity
            else:
                self.phase("down")

        if self.mv_right:
            if not self.check_collision("right"):
                if self.x <= 380:
                    self.x += self.velocity
                elif background.x + background_img.get_width() > width:
                    move_environment(all_environment, "right")
                elif self.x + self.velocity + player_img.get_width() < width:
                    self.x += self.velocity
            else:
                self.phase("right")

        elif self.mv_left:
            if not self.check_collision("left"):
                if self.x >= 320:
                    self.x -= self.velocity
                elif background.x < 0:
                    move_environment(all_environment, "left")   
                elif self.x - self.velocity > 0:
                    self.x -= self.velocity
            else:
                self.phase("left")
        po1.check_pick_up()
        po2.check_pick_up()
        self.velocity = self.default_speed
        self.colliding = False
        self.rect.topleft = (self.x, self.y)


    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def check_diagonal(self):
        if self.mv_up or self.mv_down:
            if self.mv_left or self.mv_right:
                return True
        return False
    
    def check_collision(self, direction: str):
        direction_to_coords = {
            "up": (0, -self.velocity),
            "down": (0, self.velocity), 
            "right": (self.velocity, 0),
            "left": (-self.velocity, 0)
                }
        temp_coords = (self.rect.topleft[0] + direction_to_coords[direction][0], self.rect.topleft[1] + direction_to_coords[direction][1])
        self.rect.topleft = temp_coords
        for object in all_environment:
            if object.collide:
                if self.rect.colliderect(object.rect):
                    return True
        return False
    
    def phase(self, direction):
        success = False
        if self.phase_count > 0 and self.phase_key:
            if direction == "up" and self.y > 150:
                screen.blit(anim_vert, (self.x, self.y))
                self.y -= 120
                success = True
            elif direction == "down" and self.y < height - 150:
                screen.blit(anim_vert, (self.x, self.y))
                self.y += 120
                success = True
            elif direction == "right" and self.x < width - 150:
                self.x += 120
                success = True
            elif direction == "left" and self.x > 150:
                self.x -= 120
                success = True
            if success:
                self.phase_count -= 1
            self.phase_key = False
                    


class Environment:
    def __init__(self, x, y, image, collide=True):
        self.x = x
        self.y = y
        self.image = image
        self.collide = collide
        self.rect = image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, direction):
        if direction == "up":
            self.y += player.velocity
        elif direction == "down":
            self.y -= player.velocity
        elif direction == "right":
            self.x -= player.velocity
        elif direction == "left":
            self.x += player.velocity
        self.rect.topleft = (self.x, self.y)

class PhaseOrb:
    def __init__(self, x, y, image, collide=False):
        self.x = x
        self.y = y
        self.image = image
        self.collide = collide
        self.rect = image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.colliding = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, direction):
        if direction == "up":
            self.y += player.velocity
        elif direction == "down":
            self.y -= player.velocity
        elif direction == "right":
            self.x -= player.velocity
        elif direction == "left":
            self.x += player.velocity
        self.rect.topleft = (self.x, self.y)

    def check_pick_up(self):
        if self.rect.colliderect(player.rect):
            if self.colliding == False:
                self.change_coords()
                self.rect.topleft = (self.x, self.y)
                player.phase_count += 1
                self.colliding = True
                print(player.phase_count)
        else: 
            self.colliding = False

    def change_coords(self):
        top_left_x = round(background.x + (250 - self.image.get_width())/2)
        top_left_y = round(background.y + (250 - self.image.get_width())/2)
        self.x = randrange(top_left_x, top_left_x + 250*9, 250)
        self.y = randrange(top_left_y, top_left_y + 250*8, 250)


player = Player(330, 330, 6, player_img)
background = Environment(-500, -500, background_img, False)

po1 = PhaseOrb(randrange(93, 593, 250), randrange(93, 593, 250), orb_img)
po2 = PhaseOrb(randrange(93, 593, 250), randrange(93, 593, 250), orb_img)

all_environment = [background, po1, po2]

img_choice = [vert_img, hor_img]
for index in range(80):
    object = Environment(randrange(-520, 1980, 250), randrange(-516, 1984, 250), choice(img_choice))
    all_environment.append(object)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.mv_up = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.mv_down = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.mv_right = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.mv_left = True
            if event.key == pygame.K_r:
                player.phase_key = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.mv_up = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.mv_down = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.mv_right = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.mv_left = False
            if event.key == pygame.K_r:
                player.phase_key = False

    screen.fill((0, 0, 0))

    
    
    for object in all_environment:
        object.draw()

    player.draw()
    player.move()


    pygame.display.flip()

    clock.tick(90)