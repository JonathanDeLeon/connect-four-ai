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

def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move


def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None

def alphabeta_player(game, state):
    return alphabeta_search(state, game)


# Importing Ethan's old code


def calculate_complex_heuristic(board):
    total = 0
    for i in range(0, 4):
        total = total + 2 if i + int(board[i] or 0) == 3 else 1
    return total


class Game:
    def __init__(self, initial_state, ai, player):
        self.current_state = initial_state
        self.ai = ai
        self.player = player


class State:
    def __init__(self, user_board, total_board, depth=0, heuristic=0):
        self.user_board = user_board
        self.total_board = total_board
        self.children = []
        self.depth = depth
        self.heuristic = heuristic

    def __str__(self):
        return str(self.total_board)

    def generate_children(self, parent_map):
        blank_location = self.board.index(None)
        for column in range(0, 7):
            row = 0
            while row < 6:
                # If move is legal (there isn't a tile there)
                if total_board[7*column + row] == 0:
                    total_board[7*column + row] = b'1'

                row = row + 1



            if i != 3 - blank_location and i != blank_location:
                new_board = self.board[:]
                new_board[blank_location], new_board[i] = new_board[i], new_board[blank_location]
                child = State(new_board, self.depth+1)
                child.heuristic = self.depth + calculate_complex_heuristic(child.board)
                if not State.state_in_previous(parent_map, child):
                    self.children.append(child)
                    parent_map[child] = self

    @staticmethod
    def state_in_previous(parent_map, node):
        return any(
            node.board == existing.board
            for existing in parent_map
        )


def Branch_Bound_Complex_Heuristic_Solution(root_node):
    to_visit = [root_node]
    parent_map = {root_node: None}
    while(to_visit):
        node = to_visit.pop()
        if node.board == [1, 2, 3, None]:
            solution = []
            while node is not None:
                solution = [node] + solution
                node = parent_map[node]
            return solution
        node.generate_children(parent_map, complex_heuristic=True)
        to_visit = node.children + to_visit
        to_visit.sort(key=lambda x: x.heuristic, reverse=True)
    return None


if __name__ == "__main__":
    root = State([3, 1, 2, None])
    solution = Branch_Bound_Complex_Heuristic_Solution(root)
    print("Branch and Bound Complex Heuristic solution = [", end='')
    for i in solution:
        print(i, '\b, ', end='')
    print("\b\b]")