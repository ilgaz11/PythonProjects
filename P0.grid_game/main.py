#player can go through the wall while going right sometimes

import pygame
from random import randrange, choice

pygame.init()
width, height = 1014, 676
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load("P0.grid_game/background.png")

points_font = pygame.font.SysFont("Adobe Heiti Std Normal", 32)
lost_font = pygame.font.SysFont("Adobe Heiti Std Normal", 128)


clock = pygame.time.Clock()

coin = pygame.image.load("P0.grid_game/point.png")
coin = pygame.transform.scale(coin, (40, 40))
coins_amt = 3
coins = []
for i in range(coins_amt):
    coins.append([randrange(150, width, 113), randrange(150, height, 113)])
points = 0

player = pygame.image.load("P0.grid_game/ball.png")
player_x = 11
player_y = 7
go_left = False
go_right = False
go_up = False
go_down = False
player_velocity = 113
player_stamina = 0
reset_p_stam = 4

enemy = pygame.image.load("P0.grid_game/enemy.png")
enemy = pygame.transform.scale(enemy, (80, 80))

enemy_x = randrange(128, width, 113)
enemy_y = randrange(578, height, 113)
enemy_velocity = 113
enemy_stamina = 0
reset_e_stam = 12

wall_1 = pygame.image.load("P0.grid_game/wall_1.png")
wall_2 = pygame.image.load("P0.grid_game/wall_2.png")
wall_amount = 10
wall_coords = []
wall_types = []
for i in range(wall_amount):
    wall_coords.append([randrange(106, width - 180, 112), randrange(106, height - 180, 112)])
    wall_types.append(choice([wall_1, wall_2]))
no_pass_points = []
for index in range(len(wall_coords)):
    if wall_types[index] == wall_1:
        start = wall_coords[index][0]
        no_pass_points.append([start + 240/4, wall_coords[index][1] + 120])
        no_pass_points.append([start + 240*3/4, wall_coords[index][1] + 120])
    if wall_types[index] == wall_2:
        start = wall_coords[index][1]
        no_pass_points.append([wall_coords[index][0] + 115, start + 230/4])
        no_pass_points.append([wall_coords[index][0] + 115, start + 230*3/4])



lost = False


def after_image(direction: str):
    directions = {"left": [15, 0], "right": [-15, 0], "up": [0, 15], "down": [0, -15]}
    for i in range(1, 5):
        screen.blit(player, (player_x + directions[direction][0]*i, player_y + directions[direction][1]*i))


def check_for_wall(direction: str):
    directions = {"left": [-50, -5, 0, player.get_height()], "right": [player.get_width(), player.get_width() + 50, 0, player.get_height()], "up": [0, player.get_width(), -player.get_height() + 50, -5], "down": [0, player.get_width(), player.get_height() + 5, player.get_height() + 50]}
    box = [player_x + directions[direction][0], player_x + directions[direction][1], player_y + directions[direction][2], player_y + directions[direction][3]]
    for point in no_pass_points:
        if box[0] < point[0] < box[1] and box[2] < point[1] < box[3]:
            return False
    return True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(bg, (0, 0))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            go_right = True
        elif event.key == pygame.K_LEFT:
            go_left = True
        elif event.key == pygame.K_UP:
            go_up = True
        elif event.key == pygame.K_DOWN:
            go_down = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            go_right = False
        elif event.key == pygame.K_LEFT:
            go_left = False
        elif event.key == pygame.K_UP:
            go_up = False
        elif event.key == pygame.K_DOWN:
            go_down = False

    if player_stamina <= 0:
        if go_left and player_x - player_velocity > 0:
            if check_for_wall("left"):
                player_x -= player_velocity
                player_stamina = reset_p_stam
                after_image("left")
        elif go_right and player_x + player_velocity < width - player.get_width():
            if check_for_wall("right"):
                player_x += player_velocity
                player_stamina = reset_p_stam
                after_image("right")
        elif go_up and player_y - player_velocity >= 0:
            if check_for_wall("up"):
                player_y -= player_velocity
                player_stamina = reset_p_stam
                after_image("up")
        elif go_down and player_y + player_velocity < height - player.get_height():
            if check_for_wall("down"):
                player_y += player_velocity
                player_stamina = reset_p_stam
                after_image("down")

    screen.blit(player, (player_x, player_y))
    player_stamina -= 1

    for i in range(coins_amt):
        if player_x < coins[i][0] + (coin.get_width() / 2) < player_x + player.get_width():
            if player_y < coins[i][1] + coin.get_height()/2 < player_y + player.get_height():
                coins[i] = [randrange(150, width, 113), randrange(150, height, 113)]
                points += 1
    pts_text = points_font.render(f"Points: {points}", True, (255,  0, 0))
    screen.blit(pts_text, (900, 10))
    for i in range(coins_amt):
        screen.blit(coin, (coins[i][0], coins[i][1]))

    if enemy_stamina <= 0:
        if abs(enemy_x - player_x) >= abs(enemy_y - player_y):
            if enemy_x < player_x:
                enemy_x += enemy_velocity
            elif enemy_x > player_x:
                enemy_x -= enemy_velocity
            enemy_stamina = reset_e_stam
        else:
            if enemy_y < player_y:
                enemy_y += enemy_velocity
            elif enemy_y > player_y:
                enemy_y -= enemy_velocity
            enemy_stamina = reset_e_stam
    enemy_stamina -= 1

    if player_x < enemy_x + enemy.get_width()/2 < player_x + player.get_width():
        if player_y < enemy_y + enemy.get_height()/2 < player_y + player.get_height():
            lost = True

    if lost:
        lost_text = lost_font.render(f"You lost!", True, (255, 0, 0))
        screen.blit(lost_text, (width/2 - 180, (height - 170)/2))
        enemy_stamina = 1000
        player_stamina = 1000

    screen.blit(enemy, (enemy_x, enemy_y))

    for i in range(wall_amount):
        screen.blit(wall_types[i], (wall_coords[i][0], wall_coords[i][1]))

    pygame.display.flip()

    clock.tick(60)
