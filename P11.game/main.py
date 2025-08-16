import pygame
import math
from random import randint, randrange, choice

pygame.init()

width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GAME")

clock = pygame.time.Clock()

player_img = pygame.transform.scale(pygame.image.load("Images/player.png"), (48, 48)).convert_alpha()
background_img = pygame.transform.scale(pygame.image.load("Images/bg_test.png"), (2000, 1750)).convert_alpha()
obstacle_img = pygame.transform.scale(pygame.image.load("Images/obstacle.png"), (64, 64)).convert_alpha()
vert_img = pygame.transform.scale(obstacle_img, (48, 250)).convert_alpha()
hor_img = pygame.transform.scale(obstacle_img, (250, 48)).convert_alpha()


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
        


    def move(self):
        if self.check_diagonal():
            self.velocity = self.diag_vel
        if self.mv_up and not self.check_collision("up"):
            if self.y >= 320:
                self.y -= self.velocity
            elif background.y <= 0:
                move_environment(all_environment, "up")
            elif self.y - self.velocity > 0:
                self.y -= self.velocity
        elif self.mv_down and not self.check_collision("down"):
            if self.y <= 380:
                self.y += self.velocity
            elif background.y + background_img.get_height() > height:
                move_environment(all_environment, "down")
            elif self.y + self.velocity + player_img.get_height() < height:
                self.y += self.velocity
        if self.mv_right and  not self.check_collision("right"):
            if self.x <= 380:
                self.x += self.velocity
            elif background.x + background_img.get_width() > width:
                move_environment(all_environment, "right")
            elif self.x + self.velocity + player_img.get_width() < width:
                self.x += self.velocity
        elif self.mv_left and not self.check_collision("left"):
            if self.x >= 320:
                self.x -= self.velocity
            elif background.x < 0:
                move_environment(all_environment, "left")   
            elif self.x - self.velocity > 0:
                self.x -= self.velocity
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



player = Player(330, 330, 5, player_img)
background = Environment(-500, -500, background_img, False)
ob1 = Environment(random_coords(), random_coords(), obstacle_img)
ob2 = Environment(random_coords(), random_coords(), obstacle_img)
ob3 = Environment(random_coords(), random_coords(), obstacle_img)
ob4 = Environment(-250, -250, obstacle_img)
ob5 = Environment(0, -250, obstacle_img)
ob6 = Environment(500, -250, obstacle_img)

all_environment = [background]

img_choice = [vert_img, hor_img]
for index in range(58):
    object = Environment(randrange(-500, 1500, 250), randrange(-500, 1500, 250), choice(img_choice))
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
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.mv_up = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.mv_down = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.mv_right = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.mv_left = False

    screen.fill((0, 0, 0))

    
    
    for object in all_environment:
        object.draw()

    player.draw()
    player.move()


    pygame.display.flip()

    clock.tick(90)