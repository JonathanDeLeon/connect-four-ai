#!/usr/bin/env python3
# Jonathan De Leon && Ethan Beaver
# CPTR 430 Artificial Intelligence
# Final Project
# June 6, 2018
#
# Problem:
# Create a Connect Four game and implement an AI bot that uses minimax algorithm with alpha-beta pruning

import random

infinity = float('inf')


def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None


def alphabeta_player(game, state):
    return alphabeta_search(state, game)


# Importing Ethan's old code


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


def calculate_heuristic(ai_board, total_board, depth):
    if is_winning_state(ai_board):
        return 22
    elif is_winning_state(ai_board ^ total_board):
        return -22
    else:
        return None


def is_winning_state(board):
    # Horizontal check
    m = board & (board >> 7)
    if m & (m >> 14):
        return True
    # Diagonal \
    m = board & (board >> 6)
    if m & (m >> 12):
        return True
    # Diagonal /
    m = board & (board >> 8)
    if m & (m >> 16):
        return True
    # Vertical
    m = board & (board >> 1)
    if m & (m >> 2):
        return True
    # Nothing found
    return False


def make_move(position, mask, col):
    new_position = position ^ mask
    new_mask = mask | (mask + (1 << (col * 7)))
    return new_position, new_mask


class State:
    def __init__(self, ai_board, total_board, depth=0, heuristic=0, user_turn=0):
        self.ai_board = ai_board
        self.total_board = total_board
        self.children = []
        self.depth = depth
        self.heuristic = heuristic

    # def __str__(self):
    #     return str(self.total_board)

    def generate_children(self, parent_map):
        if self.depth > 4:
            return
        for column in range(0, 7):
            row = 0
            while row < 6:
                # If move is legal (there isn't a tile there)
                if not self.total_board & (1 << (7 * column + row)):
                    new_ai_board, new_total_board = make_move(self.ai_board, self.total_board, column)

                    new_state = State(new_ai_board, new_total_board, self.depth + 1, None)
                    new_state.heuristic = calculate_heuristic(new_state.ai_board, new_state.total_board,
                                                              new_state.depth)
                    self.children.append(new_state)
                    parent_map[new_state] = self
                    row = 6
                row = row + 1


def build_tree(root_node):
    to_visit = [root_node]
    parent_map = {root_node: None}
    while to_visit:
        node = to_visit.pop()
        # Propagate heuristic upward
        if node.heuristic is not None:
            old_node = node
            parent = parent_map[node]
            while parent is not None:
                # If MAX node
                if parent.depth % 2 == 0:
                    if parent.heurstic is None or parent.heuristic <= node.heuristic:
                        parent.heuristic = node.heuristic
                # If MIN node
                else:
                    if parent.heurstic is None or parent.heuristic >= node.heuristic:
                        parent.heuristic = node.heuristic
                node = parent
                parent = parent_map[node]
            node = old_node

        node.generate_children(parent_map)
        to_visit = node.children + to_visit
    return root_node


if __name__ == "__main__":
    root = State(0, 0)
    solution = build_tree(root)
    print([h.heuristic for h in solution.children])

    # game = Game()
    # print(game.query_player())
