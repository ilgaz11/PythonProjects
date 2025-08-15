import pygame
import math

pygame.init()

width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GAME")

clock = pygame.time.Clock()

player_img = pygame.transform.scale(pygame.image.load("Images/player.png"), (64, 64)).convert_alpha()
background_img = pygame.transform.scale(pygame.image.load("Images/bg_test.png"), (1800, 1800)).convert_alpha()
obstacle_img = pygame.transform.scale(pygame.image.load("Images/obstacle.png"), (32, 32)).convert_alpha()


def move_environment(environment: list, direction: str):
    for object in environment:
        object.move(direction)

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


    def move(self):
        if self.check_diagonal():
            self.velocity = self.diag_vel
        if self.mv_up:
            if self.y >= 200:
                self.y -= self.velocity
            elif background.y <= 0:
                move_environment(all_environment, "up")
            elif self.y - self.velocity > 0:
                self.y -= self.velocity
        elif self.mv_down:
            if self.y <= 500:
                self.y += self.velocity
            elif background.y + background_img.get_height() > height:
                move_environment(all_environment, "down")
            elif self.y + self.velocity + player_img.get_height() < height:
                self.y += self.velocity
        if self.mv_right:
            if self.x <= 500:
                self.x += self.velocity
            elif background.x + background_img.get_width() > width:
                move_environment(all_environment, "right")
            elif self.x + self.velocity + player_img.get_width() < width:
                self.x += self.velocity
        elif self.mv_left:
            if self.x >= 200:
                self.x -= self.velocity
            elif background.x < 0:
                move_environment(all_environment, "left")   
            elif self.x - self.velocity > 0:
                self.x -= self.velocity
        self.velocity = self.default_speed


    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def check_diagonal(self):
        if self.mv_up or self.mv_down:
            if self.mv_left or self.mv_right:
                return True
        return False


class Environment:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

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


player = Player(300, 300, 7, player_img)
background = Environment(-500, -500, background_img)
ob1 = Environment(400, 400, obstacle_img)
ob2 = Environment(1000, 700, obstacle_img)
ob3 = Environment(-200, -100, obstacle_img)

all_environment = [background, ob1, ob2, ob3]

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

    clock.tick(60)