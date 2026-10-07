import random

DECK_COUNT = 1
STARTING_CHIPS = 100

SUITS = {
    0: "Spades",
    1: "Hearts",
    2: "Clubs",
    3: "Diamonds"
}


class Deck:
    def __init__(self):
        self._cards = []

        for _ in range(DECK_COUNT):
            for i in range(1, 14):
                for j in range(4):
                    self._cards.append([i, j])

        self.shuffle()

    def shuffle(self):
        random.shuffle(self._cards)
        self._index = 0

    def draw(self):
        if self._index >= len(self._cards):
            return -1

        card = self._cards[self._index]
        self._index += 1
        return card


class Actor:
    def __init__(self):
        self.reset()

    def add_to_hand(self, card):
        if card==-1:
            return -1
        self._hand.append(card)
        self.update_score()
    
    def get_score(self):
        return self._score

    def reset(self):
        self._hand = []
        self._score = 0
        self._bust = False

    def get_top_card(self):
        return self._hand[-1]

    def is_bust(self):
        return self._bust

    def get_hand(self):
        return self._hand

    def update_score(self):
        self._score = 0
        ace_count = 0

        for card in self._hand:
            rank = card[0]

            if rank == 1:
                self._score += 11
                ace_count += 1
            else:
                self._score += min(rank, 10)

        while self._score > 21 and ace_count > 0:
            self._score -= 10
            ace_count -= 1

        self._bust = self._score > 21


class Dealer(Actor):
    def showdown(self, deck):
        while self._score < 17:
            if self.add_to_hand(deck.draw())==-1:
                break

        return self._score


class Player(Actor):
    def __init__(self):
        super().__init__()
        self._balance = STARTING_CHIPS

    def adjust_balance(self, val):
        self._balance += val
        return self._balance

    def get_balance(self):
        return self._balance


def card_name(card):
    rank = card[0]
    suit = SUITS[card[1]]

    if rank == 1:
        rank_name = "Ace"
    elif rank == 11:
        rank_name = "Jack"
    elif rank == 12:
        rank_name = "Queen"
    elif rank == 13:
        rank_name = "King"
    else:
        rank_name = str(rank)

    return f"{rank_name} of {suit}"


def show_hand(actor):
    return ", ".join(card_name(card) for card in actor.get_hand())


def main():
    # Get number of players
    while True:
        try:
            player_count = int(input("Please input the number of players: "))

            if player_count < 1:
                print("There must be at least one player.")
                continue

            break

        except ValueError:
            print("Invalid Input.")

    players = [Player() for _ in range(player_count)]
    dealer = Dealer()

    # Main game loop
    while True:

        #New Round

        deck = Deck()
        dealer.reset()

        for player in players:
            player.reset()

        print("\n==============================")
        print("        NEW ROUND")
        print("==============================")

        #Betting

        bets = []

        for i, player in enumerate(players):
            while True:
                try:
                    print(f"\nPlayer {i + 1} has {player.get_balance()} chips.")

                    bet = int(input(
                        f"Player {i + 1}, enter your bet: "
                    ))

                    if bet <= 0:
                        print("Bet must be greater than 0.")
                    elif bet > player.get_balance():
                        print("You don't have enough chips.")
                    else:
                        break

                except ValueError:
                    print("Invalid bet.")

            player.adjust_balance(-bet)
            bets.append(bet)

        #Initial Deal

        for _ in range(2):
            dealer.add_to_hand(deck.draw())

            for player in players:
                player.add_to_hand(deck.draw())

        #Print Initial Deal Info

        print("\nDealer:")
        print(f"  {card_name(dealer.get_hand()[0])}")
        print("  [Hidden card]")

        for i, player in enumerate(players):
            print(f"\nPlayer {i + 1}:")
            print(f"  {show_hand(player)}")
            print(f"  Score: {player.get_score()}")

        #Player turns

        for i, player in enumerate(players):

            # Already have 21
            if player.get_score() == 21:
                if len(player.get_hand())==2:
                    print(f"\nPlayer {i + 1} has BLACKJACK!")
                else:
                    print(f"\nPlayer {i + 1} has 21!")
                continue

            while not player.is_bust():

                print(f"\nPlayer {i + 1}'s turn")
                print(f"Hand: {show_hand(player)}")
                print(f"Score: {player.get_score()}")

                choice = input("Hit or Stand? ").strip().lower()

                if choice == "hit":
                    card = deck.draw()

                    if card == -1:
                        print("The deck is empty.")
                        break

                    player.add_to_hand(card)

                    print(f"Drew: {card_name(card)}")

                    if player.is_bust():
                        print(
                            f"Player {i + 1} busts with "
                            f"{player.get_score()}!"
                        )

                elif choice == "stand":
                    break

                else:
                    print("Please enter 'hit' or 'stand'.")

        #Dealer turn

        print("\n==============================")
        print("        DEALER TURN")
        print("==============================")

        print(f"Dealer's hand: {show_hand(dealer)}")
        print(f"Dealer score: {dealer.get_score()}")

        if dealer.get_score() < 17:
            dealer.showdown(deck)

        print(f"Dealer's final hand: {show_hand(dealer)}")
        print(f"Dealer's final score: {dealer.get_score()}")

        if dealer.is_bust():
            print("Dealer busts!")

       #Results

        print("\n==============================")
        print("        RESULTS")
        print("==============================")

        for i, player in enumerate(players):

            score = player.get_score()
            bet = bets[i]

            if player.is_bust():
                print(f"Player {i + 1}: Bust. Lost {bet} chips.")

            elif dealer.is_bust():
                player.adjust_balance(bet * 2)
                print(
                    f"Player {i + 1}: Wins! "
                    f"Won {bet} chips."
                )

            elif score > dealer.get_score():
                player.adjust_balance(bet * 2)
                print(
                    f"Player {i + 1}: Wins! "
                    f"Won {bet} chips."
                )

            elif score == dealer.get_score():
                player.adjust_balance(bet)
                print(
                    f"Player {i + 1}: Push. "
                    f"Bet returned."
                )

            else:
                print(
                    f"Player {i + 1}: Loses. "
                    f"Lost {bet} chips."
                )

        #Show updated balances

        print("\n==============================")

        for i, player in enumerate(players):
            print(
                f"Player {i + 1}: "
                f"{player.get_balance()} chips"
            )

        #Continue?

        active_players = [
            player for player in players
            if player.get_balance() > 0
        ]

        if not active_players:
            print("\nAll players are out of chips!")
            break

        choice = input("\nPlay another round? (y/n): ").strip().lower()

        if choice != "y":
            break


if __name__ == "__main__":
    main()

#WWW: supports multiple player, concise implementation, addicting lol
#EBI: bets were attached to players, deck run out check on initial deal,dynamic deck count, deck pierce, card count tutorial bs, but honestly idc atp