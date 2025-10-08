import pygame, sys
from random import randrange

pygame.init()

#set width and height of screen
WIDTH, HEIGHT = 700, 700

WALL_AMOUNT = 3
WALL_DEFAULT_VELOCITY = 4


#gap between top and bottom pipe, 740 on normal mode
wall_gap = 740
#x value of first wall

#initialize screen and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

#create score font
score_font = pygame.font.SysFont("impact", 32)


def score_text():
	text = score_font.render(f"Score: {game.score}", True, (255, 255, 255))
	screen.blit(text, (550, 10))

def initialize_walls():
	wall_x_value = 800
	wall_list = []

	for i in range(WALL_AMOUNT):
		wall_y_value = randrange(250, 650)
		wall_y2_value = wall_y_value - wall_gap
		wall_list.append(Wall(wall_x_value, wall_y_value, bottom_wall, 2*i))
		wall_list.append(Wall(wall_x_value, wall_y2_value, bottom_wall, 2*i + 1))
		wall_x_value += 400
		#print(i)

	return wall_list

def reset_game():
	game.score = 0
	player.is_alive = True
	player.x = 300
	game.bg_x = -40


#create clock object
clock = pygame.time.Clock()

#get all images from images folder
sky_background = pygame.image.load("images/sky_bg.jpg").convert_alpha()
#sky_background = pygame.transform.scale(sky_background, (1000, 950)).convert_alpha()
bottom_wall = pygame.image.load("images/wall_image.png").convert_alpha()
bottom_wall = pygame.transform.scale(bottom_wall, (80, 500)).convert_alpha()
player_img = pygame.image.load("images/player_img.png").convert_alpha()
start_btn_image = pygame.image.load("images/start_button1.png").convert_alpha()
start_btn_image = pygame.transform.scale(start_btn_image, (250, 250))

class Button:
	def __init__(self, x, y, image):
		self.x = x
		self.y = y
		self.image = image
		self.clicked = False
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.x, self.y)
		

	def draw(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				game.walls.clear()
				game.walls = initialize_walls()
				reset_game()
		screen.blit(self.image, (self.x, self.y))
		

#create class for player
class Player:
	def __init__(self, x, y, image):
		self.x = x
		self.y = y
		self.image = image
		self.jump_timer = 0
		self.jump_cooldown = False
		#force of gravity on player
		self.gravity_effect = 2
		#create rect on object
		self.rect = self.image.get_rect()
		self.is_alive = True
		

	#draw player on screen
	def draw(self):
		screen.blit(self.image, (self.x, self.y))
	
	#def jump(self):
		#while self.jump_timer < 0:
			#self.jump_action()

	#apply gravity on player with increasing rate
	def gravity(self):
		#end game if player is too high
		if self.y < -40:
			self.is_alive = False
		#apply gravity and increase gravitational effect
		elif self.y < 640 and self.is_alive:
			self.gravity_effect += 2
			self.y += self.gravity_effect
		#end game if player is too low
		elif self.y >= 640:
			self.is_alive = False

	#make player jump
	def jump_action(self):
		self.y -= self.jump_timer
		if self.jump_timer == 5:
			self.jump_timer = 0
			self.jump_cooldown = False
		else: 
			self.jump_timer -= 10
		self.gravity_effect = 2
		self.rect.topleft = (self.x, self.y)

		


#create wall class
class Wall:
	def __init__(self, x, y, image, index):
		self.x = x
		self.y = y
		self.image = image
		self.velocity = 4
		self.index = index
		#create rect for object
		self.rect = self.image.get_rect()
		self.passed = False


	def move(self):
		#move wall right of screen if it has left the screen from left side
		if self.x < -90:
			if self.index % 2 == 0:
				y_value_reset = randrange(250, 650)
			else: 
					y_value_reset = game.walls[self.index - 1].y - wall_gap
					#print(y_value_reset)
			
			self.x = WIDTH + 400
			self.y = y_value_reset
			self.passed = False
		else:
			self.x -= self.velocity
		self.rect.topleft = (self.x, self.y)

	#draw wall on screen
	def draw(self):
		screen.blit(self.image, (self.x, self.y))

	#check if player is colliding with wall
	def check_collision(self):
		if self.rect.colliderect(player.rect):
			player.is_alive = False

	#add point to score if player is past wall
	def check_passed(self):
		if self.index % 2 == 0:
			if not self.passed and self.x < 280:
				game.score += 1
				self.passed = True
			


class Game: 
	def __init__(self, walls):
		self.score = 0
		self.walls = walls
		self.bg_x = bg_x
		self.bg_velocity = 0.5

	def move_background(self):
		if player.is_alive:
			self.bg_x -= 0.5
			



player = Player(300, 350, player_img)



start_button = Button(200, 200, start_btn_image)



#create empty wall list
wall_list = initialize_walls()

#add top and bottom wall to wall list 


bg_x = -40

game = Game(wall_list)
    

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if not player.jump_cooldown:
					player.jump_cooldown = True
					player.jump_timer = 55

	
	if player.jump_timer > 0:
		player.jump_action()
		#print(player.jump_timer)

	screen.blit(sky_background, (game.bg_x, -150))
	game.move_background()

	#draw and move player
	player.draw()
	player.gravity()


	#wall1.draw()
	#wall1.move()

	#iterate through each wall in list
	if player.is_alive:
		for wall in game.walls:
			wall.draw()
			wall.move()
			wall.check_collision()
			wall.check_passed()
			#print(wall.x)
	else: 
		player.gravity_effect = 0
		player.y = 350
		for wall in wall_list:
			wall.velocity = 0
		start_button.draw()

	

	
	#display score on screen
	score_text()



	#update screen
	pygame.display.flip()

	#framerate
	clock.tick(40)
