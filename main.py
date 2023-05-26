# In-between GitHub

from random import shuffle


# function
def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


class Card:
    suits = ["Diamonds",
             "Clubs",
             "Hearts",
             "Spades"]

    values = [None, "Ace", "2", "3", "4",
              "5", "6", "7", "8", "9", "10",
              "Jack", "Queen", "King"]

    def __init__(self, s, v):
        self.suit = s
        self.value = v

    def __lt__(self, c2):
        if self.value < c2.value:
            return True
        return False

    def __eq__(self, c2):
        if self.value == c2.value:
            return True
        return False

    def __gt__(self, c2):
        if self.value > c2.value:
            return True
        return False

    def __repr__(self):
        v = self.values[self.value] + \
            " of " + \
            self.suits[self.suit]
        return v


class Deck:
    def __init__(self, n=1):
        self.cards = []
        self.n = n
        for i in range(4):
            for j in range(1, 14):
                self.cards.append(Card(i, j))
        shuffle(self.cards)
        if n == 1:
            pass
        elif n == 2:
            self.cards.extend(self.cards)
            shuffle(self.cards)
        else:
            raise TypeError("Invalid argument. Expecting 1 or 2.")

    def rm_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()

    def reset(self):
        self.cards = []
        for i in range(4):
            for j in range(1, 14):
                self.cards.append(Card(i, j))
        shuffle(self.cards)
        if self.n == 1:
            pass
        elif self.n == 2:
            self.cards.extend(self.cards)
            shuffle(self.cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.winnings = 0

    def refill_pot(self, min_bet):
        self.winnings -= min_bet


class Pool:
    def __init__(self):
        self.value = 0

    def add_money(self, min_bet, n_players):
        self.value += min_bet * n_players


class Game:
    def __init__(self, max_players, min_bet, penalty):
        self.max_players = max_players
        self.min_bet = min_bet
        self.penalty = penalty
        self.players = []

        while True:
            n_players = get_integer_input(f"Number of players (max {max_players}):")
            if n_players <= max_players:
                break
            pass
        # initiate player names
        for i in range(n_players):
            while True:
                name = input(f"Player {i+1} name: ")
                if len(name) == 0:
                    print("Player name can't be empty")
                else:
                    self.players.append(Player(name))
                    break

        # initiate deck
        self.deck = Deck(2)

        # initiate pool
        self.pool = Pool()

    # announce high and low cards drawn by players
    @staticmethod
    def draw(pn, c_high, c_low):
        s = "***Player: {}***\nHigh card: {}\nLow card: {}"
        s = s.format(pn, c_high, c_low)
        print(s)

    # announce card drawn by players
    @staticmethod
    def player_draw(pn, pc):
        s = "{} drew {}"
        s = s.format(pn, pc)
        print(s)

    # announce winnings
    @staticmethod
    def wins(player, winnings, total_winnings):
        if winnings > 0:
            outcome = "won"
        else:
            outcome = "lost"
        s = "***{} {} {} this round***\n***Total winnings: {}***"
        s = s.format(player, outcome, winnings, total_winnings)
        print(s)

    def end_game(self):
        print("\n***GAME END***")
        for i in range(len(self.players)):
            self.players[i].winnings += self.pool.value / len(self.players)
            s = "{} winnings: {}"
            s = s.format(self.players[i].name, f"{self.players[i].winnings:.2f}")
            print(s)
        self.pool.value = 0

    def play_game(self):
        print("\n***GAME START***")

        # minimum bet
        min_bet = self.min_bet

        # initiate player turn
        p = -1

        # loop while enough cards
        while True:
            # reset player turn to first player after last player
            if p == len(self.players):
                p = 0
            else:
                p += 1

            # reset deck when not enough
            if len(self.deck.cards) < 3:
                self.deck.reset()
                print("[Deck Shuffled]\n")

            # input player response
            response = input("q to quit, s to shuffle, any key to play:\n")
            if response == 'q':
                self.end_game()
                break
            elif response == 's':
                self.deck.reset()
                print("[Deck Shuffled]\n")

            # refill pool if not enough
            if self.pool.value < (min_bet * len(self.players)):
                self.pool.add_money(min_bet, len(self.players))
                for i in range(len(self.players)):
                    self.players[i].refill_pot(min_bet)
                print("$$$Pool refilled$$$\n")

            # draw cards
            c1 = self.deck.rm_card()
            c2 = self.deck.rm_card()
            c_high = max(c1, c2)
            c_low = min(c1, c2)

            # let player decide if they want to bet
            while True:
                # reset to first player after last player
                if p == len(self.players):
                    p = 0
                # print cards drawn by players
                self.draw(self.players[p].name, c_high, c_low)
                # print players total winnings
                print(f"Total winnings: {self.players[p].winnings}")
                # print cards left
                print("Cards left: ", len(self.deck.cards))
                # print pool money
                print(f"Pool money: {self.pool.value}\n")

                # get player response on bet
                response = input(f"Bet (enter) or pass (p, penalty: {self.penalty}). Press q to quit.\n")
                if response not in ['', 'p', 'q']:
                    print("Invalid input")
                    pass
                elif response == '':
                    break
                elif response == 'p':
                    # incur penalty
                    s = "{} passed. Penalty: {}\n"
                    s = s.format(self.players[p].name, self.penalty)
                    print(s)
                    self.players[p].winnings -= self.penalty
                    self.pool.value += self.penalty
                    # reset deck if not enough cards
                    if len(self.deck.cards) < 3:
                        self.deck .reset()
                        print("[Deck Shuffled]\n")
                    else:
                        while True:
                            s = input("Shuffle deck (s)? Any key to continue.\n")
                            if s == 's':
                                self.deck.reset()
                                print("[Deck Shuffled]\n")
                            else:
                                break

                    # change players
                    p += 1
                    # draw cards
                    c1 = self.deck.rm_card()
                    c2 = self.deck.rm_card()
                    c_high = max(c1, c2)
                    c_low = min(c1, c2)
                else:
                    break

            if response == 'q':
                self.end_game()
                break

            # place bet in pool
            while True:
                bet = get_integer_input(f"Place bet (min: {min_bet}, max = {self.pool.value}):\n")
                if self.pool.value >= bet >= min_bet:
                    break
                pass

            # determine win/lose
            pc = self.deck.rm_card()
            self.draw(self.players[p].name, c_high, c_low)  # print high and low cards drawn by players
            self.player_draw(self.players[p].name, pc)  # print card drawn by players

            if c_high > pc > c_low:
                winnings = bet
            elif pc == c_high or pc == c_low:
                winnings = -2 * bet
            else:
                winnings = -bet

            # add winnings to players
            self.players[p].winnings += winnings
            # deduct winnings from pool
            self.pool.value -= winnings
            # announce outcome
            self.wins(self.players[p].name, winnings, self.players[p].winnings)

            # print pool money
            print(f"***Pool money: {self.pool.value}***\n")


g1 = Game(10, 5, 2)
g1.play_game()
