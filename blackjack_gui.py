import tkinter as tk
from tkinter import messagebox

from blackjack import Deck, Player, Dealer, card_name, show_hand


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("800x650")
        self.root.resizable(False, False)

        self.players = []
        self.dealer = Dealer()

        self.deck = None
        self.bets = []
        self.current_player = 0

        self.setup_screen()

    # Setup

    def setup_screen(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="BLACKJACK",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=30)

        label = tk.Label(
            self.root,
            text="Number of players:",
            font=("Arial", 16)
        )
        label.pack(pady=10)

        self.player_entry = tk.Entry(
            self.root,
            font=("Arial", 16),
            justify="center"
        )
        self.player_entry.pack()

        self.player_entry.focus()

        start_button = tk.Button(
            self.root,
            text="Start Game",
            font=("Arial", 16),
            width=15,
            command=self.start_game
        )
        start_button.pack(pady=30)

    def start_game(self):
        try:
            player_count = int(self.player_entry.get())

            if player_count < 1:
                print("There must be at least one player.")
                return

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid number of players."
            )
            return

        self.players = [Player() for _ in range(player_count)]

        self.start_round()

    # Main game loop

    def start_round(self):

        # New Round

        self.deck = Deck()
        self.dealer.reset()

        for player in self.players:
            player.reset()

        self.bets = []
        self.current_player = 0

        self.show_betting_screen()

    # Betting

    def show_betting_screen(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="PLACE YOUR BETS",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=20)

        self.bet_entries = []

        for i, player in enumerate(self.players):
            frame = tk.Frame(self.root)
            frame.pack(pady=8)

            label = tk.Label(
                frame,
                text=f"Player {i + 1} - {player.get_balance()} chips",
                font=("Arial", 14)
            )
            label.pack(side="left", padx=10)

            entry = tk.Entry(
                frame,
                width=8,
                font=("Arial", 14),
                justify="center"
            )
            entry.pack(side="left")

            self.bet_entries.append(entry)

        button = tk.Button(
            self.root,
            text="Deal Cards",
            font=("Arial", 16),
            width=15,
            command=self.place_bets
        )
        button.pack(pady=30)

    def place_bets(self):
        bets = []

        for i, player in enumerate(self.players):
            try:
                bet = int(self.bet_entries[i].get())

                if bet <= 0:
                    messagebox.showerror(
                        "Invalid Bet",
                        "Bet must be greater than 0."
                    )
                    return

                if bet > player.get_balance():
                    messagebox.showerror(
                        "Invalid Bet",
                        f"Player {i + 1} does not have enough chips."
                    )
                    return

            except ValueError:
                messagebox.showerror(
                    "Invalid Bet",
                    f"Invalid bet for Player {i + 1}."
                )
                return

            player.adjust_balance(-bet)
            bets.append(bet)

        self.bets = bets

        self.initial_deal()

    # Initial Deal

    def initial_deal(self):
        for _ in range(2):
            dealer_card = self.deck.draw()
            self.dealer.add_to_hand(dealer_card)

            for player in self.players:
                player_card = self.deck.draw()
                player.add_to_hand(player_card)

        self.current_player = 0

        self.show_player_turn()

    # Player turns

    def show_player_turn(self):

        # Skip players who already have 21

        while self.current_player < len(self.players):

            player = self.players[self.current_player]

            if player.is_bust():
                self.current_player += 1
                continue

            if player.get_score() == 21:
                self.current_player += 1
                continue

            break

        if self.current_player >= len(self.players):
            self.dealer_turn()
            return

        self.clear_window()

        player = self.players[self.current_player]

        title = tk.Label(
            self.root,
            text=f"PLAYER {self.current_player + 1}'S TURN",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=15)

        # Dealer

        dealer_frame = tk.LabelFrame(
            self.root,
            text="Dealer",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=10
        )
        dealer_frame.pack(pady=10)

        dealer_card = card_name(
            self.dealer.get_hand()[0]
        )

        tk.Label(
            dealer_frame,
            text=f"{dealer_card}\n[Hidden card]",
            font=("Arial", 14)
        ).pack()

        # Player

        player_frame = tk.LabelFrame(
            self.root,
            text=f"Player {self.current_player + 1}",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=10
        )
        player_frame.pack(pady=10)

        tk.Label(
            player_frame,
            text=show_hand(player),
            font=("Arial", 14),
            wraplength=700
        ).pack()

        tk.Label(
            player_frame,
            text=f"Score: {player.get_score()}",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Buttons

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        hit_button = tk.Button(
            button_frame,
            text="HIT",
            font=("Arial", 18, "bold"),
            width=10,
            height=2,
            command=self.hit
        )
        hit_button.pack(side="left", padx=10)

        stand_button = tk.Button(
            button_frame,
            text="STAND",
            font=("Arial", 18, "bold"),
            width=10,
            height=2,
            command=self.stand
        )
        stand_button.pack(side="left", padx=10)

    def hit(self):
        player = self.players[self.current_player]

        card = self.deck.draw()

        if card == -1:
            messagebox.showerror(
                "Deck Empty",
                "The deck is empty."
            )
            return

        player.add_to_hand(card)

        if player.is_bust():
            messagebox.showinfo(
                "Bust!",
                f"Player {self.current_player + 1} busts with "
                f"{player.get_score()}!"
            )

            self.current_player += 1
            self.show_player_turn()
            return

        if player.get_score() == 21:
            messagebox.showinfo(
                "21!",
                f"Player {self.current_player + 1} has 21!"
            )

            self.current_player += 1
            self.show_player_turn()
            return

        self.show_player_turn()

    def stand(self):
        self.current_player += 1
        self.show_player_turn()

    # Dealer turn

    def dealer_turn(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="DEALER TURN",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        self.update_dealer_display()

        self.root.after(1000, self.dealer_draw_step)

    def update_dealer_display(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="DEALER TURN",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        dealer_frame = tk.LabelFrame(
            self.root,
            text="Dealer",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=20
        )
        dealer_frame.pack(pady=20)

        tk.Label(
            dealer_frame,
            text=show_hand(self.dealer),
            font=("Arial", 16),
            wraplength=700
        ).pack()

        tk.Label(
            dealer_frame,
            text=f"Score: {self.dealer.get_score()}",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

    def dealer_draw_step(self):

        if self.dealer.get_score() >= 17:
            self.show_results()
            return

        card = self.deck.draw()

        if card == -1:
            self.show_results()
            return

        self.dealer.add_to_hand(card)

        self.update_dealer_display()

        self.root.after(1000, self.dealer_draw_step)

    # Results

    def show_results(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="RESULTS",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        # Dealer

        dealer_frame = tk.LabelFrame(
            self.root,
            text="Dealer",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=10
        )
        dealer_frame.pack(pady=10)

        tk.Label(
            dealer_frame,
            text=show_hand(self.dealer),
            font=("Arial", 14),
            wraplength=700
        ).pack()

        tk.Label(
            dealer_frame,
            text=f"Score: {self.dealer.get_score()}",
            font=("Arial", 16, "bold")
        ).pack()

        if self.dealer.is_bust():
            tk.Label(
                dealer_frame,
                text="DEALER BUST!",
                font=("Arial", 16, "bold")
            ).pack()

        # Player results

        for i, player in enumerate(self.players):

            score = player.get_score()
            bet = self.bets[i]

            if player.is_bust():
                result = (
                    f"Player {i + 1}: Bust. "
                    f"Lost {bet} chips."
                )

            elif self.dealer.is_bust():
                player.adjust_balance(bet * 2)

                result = (
                    f"Player {i + 1}: Wins! "
                    f"Won {bet} chips."
                )

            elif score > self.dealer.get_score():
                player.adjust_balance(bet * 2)

                result = (
                    f"Player {i + 1}: Wins! "
                    f"Won {bet} chips."
                )

            elif score == self.dealer.get_score():
                player.adjust_balance(bet)

                result = (
                    f"Player {i + 1}: Push. "
                    f"Bet returned."
                )

            else:
                result = (
                    f"Player {i + 1}: Loses. "
                    f"Lost {bet} chips."
                )

            tk.Label(
                self.root,
                text=result,
                font=("Arial", 14)
            ).pack(pady=3)

        # Show updated balances

        print()

        balance_text = ""

        for i, player in enumerate(self.players):
            balance_text += (
                f"Player {i + 1}: "
                f"{player.get_balance()} chips\n"
            )

        tk.Label(
            self.root,
            text=balance_text,
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        # Continue?

        active_players = [
            player for player in self.players
            if player.get_balance() > 0
        ]

        if not active_players:
            tk.Label(
                self.root,
                text="All players are out of chips!",
                font=("Arial", 16, "bold")
            ).pack(pady=10)

            quit_button = tk.Button(
                self.root,
                text="Quit",
                font=("Arial", 14),
                width=12,
                command=self.root.destroy
            )
            quit_button.pack(pady=10)

            return

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        play_again_button = tk.Button(
            button_frame,
            text="PLAY AGAIN",
            font=("Arial", 14, "bold"),
            width=14,
            command=self.start_round
        )
        play_again_button.pack(side="left", padx=10)

        quit_button = tk.Button(
            button_frame,
            text="QUIT",
            font=("Arial", 14),
            width=14,
            command=self.root.destroy
        )
        quit_button.pack(side="left", padx=10)

    # Utility

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()

    app = BlackjackGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()

#WWW: it works and supports multiple players.
#EBI: clunky, card and chip logos, animations, unoptimized, same issues as with original, but too much work for a simple project like this. I guess this is good enough