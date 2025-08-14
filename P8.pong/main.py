import pygame, sys
from math import sin, cos, pi, sqrt
from random import randint, choice

pygame.init()

width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")
font = pygame.font.SysFont("impact", 40)
button_font = pygame.font.SysFont("impact", 46)

clock = pygame.time.Clock()

player1_img = pygame.image.load("Images/player1.png").convert_alpha()
player2_img = pygame.image.load("Images/player2.png").convert_alpha()
ball_img = pygame.image.load("Images/ball.png").convert_alpha()
bouncer_img = pygame.image.load("Images/bouncer.png").convert_alpha()
speeder_img = pygame.image.load("Images/speeder.png").convert_alpha()
button = pygame.image.load("Images/button_frame.png").convert_alpha()
title = pygame.transform.scale(pygame.image.load("Images/title.png"), (528, 132)).convert_alpha()


def deg_to_rad(angle):
    return angle*2*pi/360

class Game:
    def __init__(self):
        self.p1_pts = 0
        self.p2_pts = 0
        self.p2 = opponent
        self.start = False
        self.timer = 0

class Button:
    def __init__(self, x, y, image, text, command=None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = button_font.render(text, True, (250, 250, 250))
        self.clicked = False
        self.command = command

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                if self.command == 1:
                    game.start = True
                    game.p2 = opponent
                elif self.command == 2:
                    game.start = True
                    game.p2 = player2
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.text, (self.x + (200 - self.text.get_width())/2, self.y + 15))

class Player:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.velocity = 4
        self.image = image
        self.moving_up = False
        self.moving_down = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.moving_up and self.y >= 5:
            self.y -= self.velocity
        elif self.moving_down and self.y + player1_img.get_height() <= height - 5:
            self.y += self.velocity

class Opponent:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.image = image
        self.velocity = 4
        self.moving_up = False
        self.moving_down = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if ball.vel_x > 0:
            if ball.y < self.y + 15 and self.y >= 5:
                self.y -= self.velocity
            elif ball.y > self.y - 15 and self.y + player1_img.get_height() <= height - 5:
                self.y += self.velocity
        else: 
            if self.y > height/2:
                self.y -= self.velocity
            elif self.y < height/2:
                self.y += self.velocity


class Ball:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.image = image
        self.velocity = 7
        self.angle = deg_to_rad(20)
        self.vel_x = cos(self.angle) * self.velocity
        self.vel_y = - sin(self.angle) * self.velocity

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def play(self):
        self.move()
        self.check_out()

    def move(self):
        #up wall
        if self.y <= 0:
            self.change_angle(pi/2)
        #down wall
        elif self.y + ball_img.get_height() >= height:
            self.change_angle(3*pi/2)
        #right wall
        if self.check_collision_p2():
            self.change_angle(pi)
            self.check_moving(game.p2)
        #left wall
        elif self.check_collision_p1():
            self.change_angle(0)
            self.check_moving(player1)
        
        self.vel_x = cos(self.angle) * self.velocity
        self.vel_y = - sin(self.angle) * self.velocity

        self.x += self.vel_x
        self.y += self.vel_y

    def change_angle(self, wall: float):
        difference = pi/2 - (self.angle - wall)
        self.angle = wall + pi/2 + difference
        self.angle = self.og_angle(self.angle)

    def check_collision_p1(self):
        if self.vel_x < 0:
            if self.y + ball_img.get_height() > player1.y and self.y < player1.y + player1_img.get_height():
                if player1.x <= self.x <= player1.x + player1_img.get_width():
                    return True

    def check_collision_p2(self):
        if self.vel_x > 0:
            if self.y + ball_img.get_height() > game.p2.y and self.y < game.p2.y + player1_img.get_height():
                if game.p2.x + 15 >= self.x + ball_img.get_width() >= game.p2.x: 
                    return True

    def check_moving(self, player):
        difference = deg_to_rad(15) if player == player2 else - deg_to_rad(15)
        if player.moving_up and self.check_angle(self.angle + difference):
            self.angle += difference
        elif player.moving_down and self.check_angle(self.angle - difference):
            self.angle -= difference

    def check_out(self):
        out_left = False
        out_right = False
        if self.x < 0:
            out_left = True
            game.p2_pts += 1
        elif self.x + ball_img.get_width() > width:
            out_right = True
            game.p1_pts += 1
        if out_right or out_left:
            self.x = 150 if out_right else 750
            self.y = (height + ball_img.get_height())/2
            self.velocity = 7
            game.timer = 0
            self.angle = deg_to_rad(5) if out_right else deg_to_rad(175)

    def check_angle(self, angle):
        if angle > 0:
            while angle > 2*pi:
                angle -= 2*pi
        elif angle < 0:
            while angle < 0:
                angle += 2*pi
        if deg_to_rad(114) > angle > deg_to_rad(66):
            return False
        elif deg_to_rad(246) < angle < deg_to_rad(294):
            return False
        return True
    
    def og_angle(self, angle):
        if angle > 0:
            while angle > 2*pi:
                angle -= 2*pi
        elif angle < 0:
            while angle < 0:
                angle += 2*pi
        return angle
    
class Ability:
    def __init__(self, image, command):
        self.x = randint(200, 700)
        self.y = randint(50, 550)
        self.image = image
        self.command = command
        self.timer = 0 

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self):
        if ball.x + ball_img.get_width()/2 > self.x and ball.x + ball_img.get_width()/2 < self.x + bouncer_img.get_width():
            if ball.y + ball_img.get_height()/2 > self.y and ball.y + ball_img.get_height()/2 < self.y + bouncer_img.get_height():
                if self.command == "bouncer":
                    self.bouncer()
                elif self.command == "speeder":
                    game.timer = 180
                self.x = randint(300, 600)
                self.y = randint(100, 500)

    def bouncer(self):
        bounce = choice([-40, -27, -12, 12, 27, 40])
        if ball.check_angle(ball.angle + deg_to_rad(bounce)):
            ball.angle += deg_to_rad(bounce)
        elif ball.check_angle(ball.angle - deg_to_rad(bounce)):
            ball.angle -= deg_to_rad(bounce)
        else:
            ball.angle += deg_to_rad(choice(-5, 5)) 


player1 = Player(16, 300, player1_img)
player2 = Player(862, 300, player2_img)
opponent = Opponent(862, 300, player2_img)
ball = Ball(300, 500, ball_img)
bouncer1 = Ability(bouncer_img, "bouncer")
bouncer2 = Ability(bouncer_img, "bouncer")
speeder = Ability(speeder_img, "speeder")
abilities = [bouncer1, bouncer2, speeder]
one_player = Button(200, 250, button, "1 Player", 1)
two_players = Button(500, 250, button, "2 Players", 2)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.moving_up = True
            elif event.key == pygame.K_s:
                player1.moving_down = True
            if event.key == pygame.K_UP:
                player2.moving_up = True
            elif event.key == pygame.K_DOWN:
                player2.moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1.moving_up = False
            elif event.key == pygame.K_s:
                player1.moving_down = False
            if event.key == pygame.K_UP:
                player2.moving_up = False
            elif event.key == pygame.K_DOWN:
                player2.moving_down = False


    screen.fill((10, 10, 30))

    if game.start:
        score = font.render(f"{game.p1_pts}       |       {game.p2_pts}", True, (255, 255, 255))
        screen.blit(score, ((width - score.get_width())/2, 6))

        player1.move()
        player1.draw()

        if game.p2 == opponent:
            opponent.move()
            opponent.draw()
        elif game.p2 == player2:
            player2.move()
            player2.draw()

        ball.draw()
        ball.play()

        for ability in abilities:
            ability.draw()
            ability.check_collision()
        if game.timer == 1:
            ball.velocity = 7
        elif game.timer > 0:
            ball.velocity = 12
            game.timer -= 1
    else:
        screen.blit(title, ((width - title.get_width())/2, 20))
        one_player.draw()
        two_players.draw()


    pygame.display.flip()
    clock.tick(60)

