#!/usr/bin/env python3
# Jonathan De Leon && Ethan Beaver
# CPTR 430 Artificial Intelligence
# Final Project
# June 6, 2018
#
# Problem:
# Create a Connect Four game and implement an AI bot that uses minimax algorithm with alpha-beta pruning


class Game:
    AI = -1
    PLAYER = 0

    def __init__(self):
        self.current_state = State(0, 0)
        self.turn = self.PLAYER

    def is_game_over(self):
        if self.has_winning_state():
            """Display who won"""
            print("AI Bot won!") if self.turn == self.AI else print("Congratulations, you won!")
            return True
        elif self.draw():
            print("Draw...Thank you...come again")
            return True
        return False

    def draw(self):
        """Check current state to determine if it is in a draw"""
        return not self.has_winning_state() and all(self.current_state.game_position & (1 << (7 * column + 5)) for column in range(0, 6))

    def has_winning_state(self):
        return State.is_winning_state(self.current_state.ai_position) or State.is_winning_state(self.current_state.ai_position ^ self.current_state.game_position)

    def next_turn(self):
        if self.turn == self.AI:
            self.query_AI()
        else:
            self.query_player()

        if self.has_winning_state():
            return self.is_game_over()

        #self.turn = (self.turn + 1) % 2
        # Apply one's complement (invert bits); 0 ~= -1
        self.turn = ~self.turn

    def query_player(self):
        """Make a move by querying standard input."""
        column = None
        while column is None:
            column = input('Your move identify column [0-6]? ')
            try:
                column = int(column)
                # Check if move is legal
                if not 0 <= column <= 6:
                    raise ValueError
                if self.current_state.game_position & (1 << (7 * column + 5)):
                    raise IndexError
            except (ValueError, IndexError):
                print("Invalid move. Try again...")
                column = None
        new_position, new_game_position = make_move(self.current_state.player_position,
                                                    self.current_state.game_position, column)
        self.current_state.game_position = new_game_position
        self.current_state.depth += 1
        # self.current_state = State(new_position, new_game_position, self.current_state.depth + 1)

    def query_AI(self):
        """ AI Bot chooses next best move from current state """
        print("\nAI's Move...")
        self.current_state = alphabeta_search(self.current_state)


def make_move(position, mask, col):
    opponent_position = position ^ mask
    new_mask = mask | (mask + (1 << (col * 7)))
    return opponent_position ^ new_mask, new_mask


def make_move_opponent(position, mask, col):
    new_mask = mask | (mask + (1 << (col * 7)))
    return position, new_mask


class State:
    def __init__(self, ai_position, game_position, depth=0):
        self.ai_position = ai_position
        self.game_position = game_position
        self.depth = depth

    @property
    def player_position(self):
        return self.ai_position ^ self.game_position

    @staticmethod
    def is_winning_state(position):
        # Horizontal check
        m = position & (position >> 7)
        if m & (m >> 14):
            return True
        # Diagonal \
        m = position & (position >> 6)
        if m & (m >> 12):
            return True
        # Diagonal /
        m = position & (position >> 8)
        if m & (m >> 16):
            return True
        # Vertical
        m = position & (position >> 1)
        if m & (m >> 2):
            return True
        # Nothing found
        return False

    def terminal_test(self):
        if State.is_winning_state(self.ai_position) or State.is_winning_state(self.ai_position ^ self.game_position):
            return True
        else:
            return False

    def calculate_heuristic(self):
        if self.is_winning_state(self.ai_position):
            return 22 - self.depth
        elif self.is_winning_state(self.ai_position ^ self.game_position):
            return -1 * (22 - self.depth)
        else:
            return None

    def generate_children(self):
        """ For each column entry, generate a new State if the new position is valid"""
        for column in range(0, 7):
            if not self.game_position & (1 << (7 * column + 5)):
                new_ai_position, new_game_position = make_move(self.ai_position, self.game_position, column)
                yield State(new_ai_position, new_game_position, self.depth + 1)

    def __str__(self):
        # return str(self.game_position)
        return '{0:049b}'.format(self.game_position)


infinity = float('inf')


def alphabeta_search(state):
    """Search game state to determine best action; use alpha-beta pruning. """

    # Functions used by alpha beta
    def max_value(state, alpha, beta):
        if state.terminal_test():
            return state.calculate_heuristic()
        v = -infinity
        for child in state.generate_children():
            v = max(v, min_value(child, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if state.terminal_test():
            return state.calculate_heuristic()
        v = infinity
        for child in state.generate_children():
            v = min(v, max_value(child, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha beta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    # TODO: Debug value of v
    for child in state.generate_children():
        v = min_value(child, best_score, beta)
        print(v)
        if v > best_score:
            best_score = v
            best_action = child
    return best_action


def print_board(state):
    """
    Helper method to pretty print binary board (6x7 board with top row as sentinel row of 0's)
    -  -   -   -   -   -   -
    5  12  19  26  33  40  47
    4  11  18  25  32  39  46
    3  10  17  24  31  38  45
    2  9   16  23  30  37  44
    1  8   15  22  29  36  43
    0  7   14  21  28  35  42
    """
    ai_board, total_board = state.ai_position, state.game_position
    for row in range(5, -1, -1):
        print("")
        for column in range(0, 7):
            if ai_board & (1 << (7 * column + row)):
                print("1", end='')
            elif total_board & (1 << (7 * column + row)):
                print("2", end='')
            else:
                print("0", end='')
    print("")


if __name__ == "__main__":
    game = Game()

    print("Welcome to Connect Four!")
    print_board(game.current_state)
    while not game.is_game_over():
        game.next_turn()
        print_board(game.current_state)
