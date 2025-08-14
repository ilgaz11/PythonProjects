#improvements needed: ace counts as 10 instead of 1 or 11

from random import sample, choice

class Blackjack:
    def __init__(self):
        self.cards = []
        self.player_hand = None
        self.dealer_hand = None
        
    def reset_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        special = ["Ace", "Jack", "Queen", "King"]
        for suit in suits:
            for item in special:
                self.cards.append(f"{item} of {suit}")
            for digit in range(2, 11):
                self.cards.append(f"{digit} of {suit}")

    def deal_cards(self):
        four_cards = sample(self.cards, 4)
        self.player_hand = four_cards[:2]
        self.dealer_hand = four_cards[2:]
        self.remove_cards(four_cards)

    def remove_cards(self, used_cards: list):
        for card in used_cards:
            if card in self.cards:
                self.cards.remove(card)

    def show_hands(self):
        print("Your hand: ")
        for card in self.player_hand:
            print(card, end="    ")
        print("\n")
        print("Dealer's hand:")
        print(f"{self.dealer_hand[0]}     ???")
      
    
    def dealer_hits(self):
        added_card = choice(self.cards)
        self.dealer_hand.append(added_card)
        self.remove_cards(list(added_card))
        return self.dealer_hand

    def player_hits(self):
        added_card = choice(self.cards)
        self.player_hand.append(added_card)
        self.remove_cards(list(added_card))
        return self.player_hand

    def check_points(self, person: str):
        points = 0
        if person == "player":
            for card in self.player_hand:
                try:
                    points += int(card.split(" ")[0])
                except ValueError:
                    points += 10
        elif person == "dealer":
            for card in self.dealer_hand:
                try:
                    points += int(card.split(" ")[0])
                except ValueError:
                    points += 10
        return points

                    

    def play(self):
        print("    ==== Blackjack ==== \n")
        self.reset_deck()
        self.deal_cards()
        self.show_hands()
        while self.check_points("player") < 21:
            action = input("\nHit / Stand: ")
            if action.lower() == "stand":
                break
            elif action.lower() == "hit":
                print("New card: ", end=" ")
                print(self.player_hits()[-1])
                print(self.check_points("player"))
        if self.check_points("player") > 21:
            print("You busted!")
        else:
            print("")
            while self.check_points("dealer") < self.check_points("player") and self.check_points("dealer") < 17:
                self.dealer_hits()
            print("Dealer's hand: ")
            for i in self.dealer_hand:
                print(i)
            print(self.check_points("dealer"))
            if self.check_points("dealer") < self.check_points("player"):
                print("You win!")
            elif self.check_points("dealer") > self.check_points("player"):
                if self.check_points("dealer") > 21:
                    print("You win! Dealer busted.")
                else: 
                    print("You lose!")
            else:
                print("Tie!")



command = "1"
while True:
    print("")
    command = input("1 - Play or 0 - Quit: ")
    print("\n\n")
    Blackjack().play()
