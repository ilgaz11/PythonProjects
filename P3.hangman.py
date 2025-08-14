#improvements needed: word list is manual and not big enough

from random import choice

class Hangman:
    def __init__(self):
        self.words = ["python", "bald", "planet", "ordinary", "galaxy", "computer", "fragment", "musician", "hexagon", "industry", "football", "velocity", "aerodynamic", "presidential", "pzazz", "electronic", "saxophone", "crucial", "password", "gigantic", "ionization", "apocalypse", "horizon", "current", "curvature", "invincible"]
        self.keyword = choice(self.words)
        self.letters = [[letter, False] for letter in self.keyword]

    
    def show_code(self):
        for letter in self.letters:
            if letter[1]:
                print(letter[0].upper(), end=" ")
            else:
                print("_", end=" ")
        print("")

    def check_win(self):
        for letter in self.letters:
            if letter[1] == False:
                return False
        return True


def main():
    guesses = 6
    game = Hangman()
    guessed_letters = []
    print("=== Hangman ====")
    while guesses > 0 and not game.check_win():
        print("")
        wrong_guess = True
        game.show_code()
        guess = input("Guess a letter: ")
        if guess not in guessed_letters:
            guessed_letters.append(guess)
            for letter in game.letters:
                if guess == letter[0]:
                    letter[1] = True
                    wrong_guess = False
            if wrong_guess:
                guesses -= 1
            print(f"Guesses remaining: {guesses}")
        else:
            print("Letter already guessed.")


    if game.check_win():
        game.show_code()
        print("You win!")
    else: 
        print("You lose...")
        print(f"The word was {game.keyword}")             


if __name__ == "__main__":
    main()


    


