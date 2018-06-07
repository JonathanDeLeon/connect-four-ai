#!/usr/bin/env python3
# Jonathan De Leon && Ethan Beaver
# CPTR 430 Artificial Intelligence
# Final Project
# June 6, 2018
#
# Problem:
# Create a Connect Four game and implement an AI bot that uses minimax algorithm with alpha-beta pruning


class Game:
    AI = 0
    PLAYER = 1

    def __init__(self, initial_state):
        self.current_state = initial_state
        self.turn = self.PLAYER

    def game_over(self):
        if self.connected_four():
            """Display who won"""
            return True
        elif self.draw():
            print("Draw...Thank you...come again")
            return True
        return False

    def draw(self):
        """Check current state to determine if it is in a draw"""
        return False

    def connected_four(self):
        position = self.current_state
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

    def next_turn(self):
        if self.connected_four():
            return

        if self.turn == self.AI:
            self.query_AI()
        else:
            self.query_player()
        self.turn = self.turn % 1

    def query_player(self):
        """Make a move by querying standard input."""
        # print("current state:")
        # game.display(self.current_state)
        # print("available moves: {}".format(game.actions(self.current_state)))
        # print("")
        column = None
        while column is None:
            column = input('Your move identify column [0-6]? ')
            try:
                column = int(column)
                if not 0 <= column <= 6:
                    raise ValueError
                """Check if move is legal"""
            except ValueError:
                print("Invalid move. Try again...")
                column = None

        return column

    def query_AI(self):
        """AI Stuff"""
        alphabeta_search(self.current_state)


def make_move(position, mask, col):
    opponent_position = position ^ mask
    new_mask = mask | (mask + (1 << (col * 7)))
    return opponent_position ^ new_mask, new_mask


def make_move_opponent(position, mask, col):
    new_mask = mask | (mask + (1 << (col * 7)))
    return position, new_mask


class State:
    def __init__(self, ai_position, game_position, depth=0, heuristic=None):
        self.ai_position = ai_position
        self.game_position = game_position
        self.depth = depth
        self.heuristic = heuristic

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

    def generate_children(self):
        for column in range(0, 7):
            # row = 0
            # while row < 6:
            #     # If move is legal (there isn't a tile there)
            #     if not self.game_position & (1 << (7 * column + row)):
            #         new_ai_board, new_total_board = make_move(self.ai_position, self.game_position, column)
            #
            #         new_state = State(new_ai_board, new_total_board, self.depth + 1, None)
            #         new_state.heuristic = calculate_heuristic(new_state.ai_position, new_state.game_position,
            #                                                   new_state.depth)
            #         self.children.append(new_state)
            #         parent_map[new_state] = self
            #         row = 6
            #     row = row + 1
            if not self.game_position & (1 << (7 * column + 5)):
                new_ai_position, new_game_position = make_move(self.ai_position, self.game_position, column)
                # Before creating, check if it is a valid move or if we have seen the move before
                yield State(new_ai_position, new_game_position, self.depth + 1, None)

            # new_state = State(new_ai_board, new_total_board, self.depth + 1, None)
            # new_state.heuristic = calculate_heuristic(new_state.ai_position, new_state.game_position,
            #                                           new_state.depth)
            # self.children.append(new_state)
            # parent_map[new_state] = self

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
    for child in state.generate_children():
        v = min_value(child, best_score, beta)
        if v > best_score:
            best_score = v
            best_action = child
    print(best_score)
    return best_action


def print_board(state):
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
    root = State(0, 0)
    print_board(alphabeta_search(root))

    # game = Game()
    # print(game.query_player())
