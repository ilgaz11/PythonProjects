import pygame, sys
from random import sample


pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mastermind")
end_font = pygame.font.SysFont("impact", 40)
help_font = pygame.font.SysFont("ebrima", 21)
score_font = pygame.font.SysFont("impact", 30)
clock = pygame.time.Clock()

board = pygame.transform.scale(pygame.image.load("Images/board.png"), (240, 600)).convert_alpha()
back_board = pygame.transform.scale(pygame.image.load("Images/board_back.png"), (300, 600)).convert_alpha()

pink = pygame.image.load("Images/pink.png").convert_alpha()
orange = pygame.image.load("Images/orange.png").convert_alpha()
yellow = pygame.image.load("Images/yellow.png").convert_alpha()
green = pygame.image.load("Images/green.png").convert_alpha()
blue = pygame.image.load("Images/blue.png").convert_alpha()
purple = pygame.image.load("Images/purple.png").convert_alpha()
reset_button = pygame.image.load("Images/reset.png").convert_alpha()
guess_button = pygame.image.load("Images/guess.png").convert_alpha()
red = pygame.transform.scale(pygame.image.load("Images/red.png"), (16, 16)).convert_alpha()
white = pygame.transform.scale(pygame.image.load("Images/white.png"), (16, 16)).convert_alpha()
grey = pygame.transform.scale(pygame.image.load("Images/grey.png"), (16, 16)).convert_alpha()
help = pygame.image.load("Images/help.png").convert_alpha()
help_menu = pygame.transform.scale(pygame.image.load("Images/help_menu.png"), (640, 590)).convert_alpha()
play_again = pygame.image.load("Images/play_again.png").convert_alpha()

class Button:

    help_clicked = False

    def __init__(self, x, y, image, command=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.command = command
        
    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                #print(f"Click ({self.command})")
                if self.command == "Reset":
                    game.reset_guess()
                elif self.command == "Help":
                    if Button.help_clicked == False:
                        Button.help_clicked = True
                    else:
                        Button.help_clicked = False
                elif self.command == "Again":
                    game.reset_game()
                elif len(game.guess) == 4 and self.command == "Guess":
                    game.submit_guess()
                elif len(game.guess) < 4:
                    game.guess_colour(self.command)

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def just_draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def __str__(self):
        return f"{self.command}"

class Mastermind:
    def __init__(self):
        self.code = None
        self.colours = ["yellow", "pink", "blue", "green", "purple", "orange"]
        self.guess = []
        self.attempt = 0
        self.past_guesses = []
        self.colour_to_img = {
            "pink": pink, "orange": orange, "yellow": yellow, "green": green, "blue": blue,
            "purple": purple, "red": red, "white": white, "none": grey
            }
        self.submission = []
        self.win = False
        self.lose = False
        self.wins = 0
        self.losses = 0
        self.total_attempts = 0

    def set_code(self):
        self.code = sample(self.colours, k=4)

    def guess_colour(self, colour: str):
        if colour in self.colours:
            self.guess.append(colour)

    def reset_guess(self):
        self.guess = []   
    
    def submit_guess(self):
        right_place = 0
        right_colour = 0
        for colour in self.code:
            if colour in self.guess:
                right_index = self.code.index(colour)
                if self.guess[right_index] == colour:
                    right_place += 1
                else:
                    right_colour += 1
        for index in range(len(self.guess)):
            colour_dot = self.guess_to_colours(index)
            self.past_guesses.append(colour_dot)
        self.guess = []
        self.submission = []
        for i in range(right_place):
            self.submission.append("red")
        for i in range(right_colour):
            self.submission.append("white")
        for i in range(4 - (right_colour + right_place)):
            self.submission.append("none")
        for index in range(len(self.submission)):
            clr_dot = self.submit_to_colours(index)
            self.past_guesses.append(clr_dot)
        self.attempt += 1
        if self.submission == ["red", "red", "red", "red"]:
            self.win = True
            buttons.append(b_play_again)
            self.wins += 1
            self.total_attempts += self.attempt
        elif self.attempt > 7:
            self.lose = True
            buttons.append(b_play_again)
            self.losses += 1
            self.total_attempts += self.attempt

    def place_colours(self):
        for index in range(len(self.guess)):
            colour_dot = self.guess_to_colours(index)
            colour_dot.just_draw()

    def place_verifiers(self):
        for index in range(len(self.guess)):
            colour_dot = self.submit_to_colours(index)
            colour_dot.just_draw()

    def guess_to_colours(self, index: int):
            x = 60 + 50*index
            y = 557 - 60*self.attempt
            colour_dot = Button(x, y, self.colour_to_img[self.guess[index]], self.guess[index])
            return colour_dot

    def submit_to_colours(self, index: int):
        x = 283 if index == 0 or index == 2 else 305
        y = 565 - 60*self.attempt if index < 2 else 584 - 60*self.attempt
        colour_dot = Button(x, y, self.colour_to_img[self.submission[index]], self.submission[index])
        return colour_dot

    def reveal_code(self, code: list):
        for index in range(len(code)):
            x = 410 + 58*index
            y = 5
            colour_dot = Button(x, y, self.colour_to_img[code[index]], code[index])
            self.past_guesses.append(colour_dot)

    def reset_game(self):
        self.set_code()
        self.past_guesses = []
        self.guess = []
        self.win = False
        self.lose = False
        self.attempt = 0
        buttons.remove(b_play_again)
        print(self.code)

def render_text_lines(text: str, starting_x: int, starting_y: int):
    lines = text.split("\n")
    for index in range(len(lines)):
        rendered = help_font.render(lines[index], True, (0,0,0))
        screen.blit(rendered, (starting_x, starting_y + 20*index))

game = Mastermind()
game.set_code()
print(game.code)

b_pink = Button(400, 360, pink, "pink")
b_orange = Button(490, 360, orange, "orange")
b_yellow = Button(580, 360, yellow, "yellow")
b_green = Button(400, 430, green, "green")
b_blue = Button(490, 430, blue, "blue")
b_purple = Button(580, 430, purple, "purple")
b_reset = Button(350, 520, reset_button, "Reset")
b_guess = Button(520, 520, guess_button, "Guess")
b_help = Button(650, 4, help, "Help")
b_play_again = Button(370, 590, play_again, "Again")
buttons = [b_pink, b_orange, b_yellow, b_green, b_blue, b_purple, b_reset, b_guess, b_help]

help_msg = """
The goal is to guess the 4 colour combination in 8 guesses \n   or less\n
- The same colour cannot be in the code more than once\n
- Press guess to submit an attempt or press reset to reset\n your attempt\n\n
On the side:\n\n
            A red dot means right colour in the right spot\n\n\n
            A white dot means right colour but wrong spot\n\n
            A grey dot means wrong colour\n\n
    You will have to figure out which dot is associated\n    with which colour
    """

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #print(game.past_guesses)
            sys.exit()

    screen.fill((210, 255, 255))

    screen.blit(back_board, (40, 60))

    game.place_colours()

    if not Button.help_clicked:
        for button in buttons:
            button.draw()

    for item in game.past_guesses:
        item.just_draw()

    screen.blit(board, (40, 60))

    if game.attempt > 1:
        win_msg = end_font.render(f"You win!  ( {game.attempt} attempts )", True, (0,0,0))
    else:
        win_msg = end_font.render(f"You win!  ( {game.attempt} attempt )", True, (0,0,0))

    lose_msg = end_font.render(f"You lose...  Code: ", True, (0,0,0))
    score_text = end_font.render(f"Wins: {game.wins}    Losses: {game.losses}", True, (30,30,30))
    avg_attempts = round((0 if game.wins + game.losses == 0 else game.total_attempts / (game.wins + game.losses)), 1)
    attempts_text = score_font.render(f"Average Attempts: {avg_attempts}", True, (30,30,30))

    screen.blit(score_text, (360, 200))
    if game.win:
        screen.blit(win_msg, (170, 2))
        screen.blit(attempts_text, (370, 260))
    elif game.lose:
        screen.blit(lose_msg, (130, 2))
        game.reveal_code(game.code)
        screen.blit(attempts_text, (370, 260))


    if Button.help_clicked:
        screen.blit(help_menu, (30, 47))
        render_text_lines(help_msg, 75, 70)
        b_help.draw()

    pygame.display.flip()

    clock.tick(60)
