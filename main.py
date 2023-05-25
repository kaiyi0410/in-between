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
    def __init__(self):
        self.cards = []
        for i in range(4):
            for j in range(1, 14):
                self.cards.append(Card(i, j))
        shuffle(self.cards)

    def rm_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()


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
    def __init__(self, max_players, min_bet):
        self.max_players = max_players
        self.min_bet = min_bet
        self.players = []
        self.condition = 'play'

        while True:
            n_players = get_integer_input(f"Number of players (max {max_players}):")
            if n_players <= max_players:
                break
            pass
        # initiate player names
        for i in range(n_players):
            name = input("Player name: ")
            self.players.append(Player(name))

        # initiate deck
        self.deck = Deck()

        # initiate pool
        self.pool = Pool()

    # announce cards drawn by players
    @staticmethod
    def draw(pn, c_high, c_low):
        d = "***Player: {}***\nHigh card: {}\nLow card: {}"
        d = d.format(pn, c_high, c_low)
        print(d)

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
        w = "***{} {} {} this round***\n***Total winnings: {}***"
        w = w.format(player, outcome, winnings, total_winnings)
        print(w)

    def end_game(self):
        print("\n***GAME END***")
        for i in range(len(self.players)):
            self.players[i].winnings += self.pool.value / len(self.players)
            self.pool.value = 0
            p = "{} winnings: {}"
            p = p.format(self.players[i].name, f"{self.players[i].winnings:.2f}")
            print(p)
        self.condition = 'stop'

    def play_game(self):
        print("\n***GAME START***")

        # minimum bet
        min_bet = self.min_bet

        # initiate player turn
        p = -1

        # loop while enough cards
        while self.condition == 'play':
            # reset player turn to first player after last player
            if p == len(self.players):
                p = 0
            else:
                p += 1

            # ask if players want to continue after deck finished
            if len(self.deck.cards) < 3:
                while True:
                    response = input("Deck finished, do you wish to reset? (y/n)\n")
                    if response != 'y' or response != 'n':
                        pass
                    if response == 'y':
                        # reset deck
                        self.deck = Deck()
                        print("[Deck Shuffled]")
                        break
                    if response == 'n':
                        self.end_game()

            # input player response
            response = input("q to quit, s to shuffle, any key to play:\n")
            if response == 'q':
                self.end_game()
                break
            if response == 's':
                self.deck = Deck()
                print("[Deck Shuffled]\n")

            # check pool value
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
                response = input("Do you want to bet? (y/n) Press q to quit.\n")
                if response not in ['y', 'n', 'q']:
                    pass
                elif response == 'y':
                    break
                elif response == 'n':
                    # reset deck if not enough cards
                    if len(self.deck.cards) < 3:
                        self.deck = Deck()
                        print("[Deck Shuffled]\n")
                    # change players
                    p += 1
                    # draw cards
                    c1 = self.deck.rm_card()
                    c2 = self.deck.rm_card()
                    c_high = max(c1, c2)
                    c_low = min(c1, c2)
                else:
                    self.end_game()

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


g1 = Game(10, 5)
g1.play_game()

# issues
# option for 2 decks
