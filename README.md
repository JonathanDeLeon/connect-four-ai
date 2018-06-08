# Connect Four AI: A Minimax Approach

Project was completed for *CPTR 430 Artificial Intelligence* at Walla Walla University.

## Game Overview

Connect Four is a two player connection game on a *6x7* board. The goal of the game is to strategically insert a disk in one of the seven columns giving you a higher chance to connect 4 disks by row, column, or diagonal. Players alternate turns. 

Connect Four is a solved game. With perfect play, the first player always wins.

## Minimax with alpha-beta pruning

There are *4,531,985,219,092* possible unique states of the board. This makes it difficult to brute force the game tree. Thus, we used the minimax algorithm with alpha-beta pruning. 

Minimax contains two levels: *MAX* level and *MIN* level. The *MAX* node chooses its maximum value from its children, while the *MIN* node chooses its minimum value from its children. Alpha-beta pruning allows us to abandon *(prune)* subtrees that will not influence the final decision because its heuristic value is not within the boundary window between alpha and beta. 

Alpha is the lower bound where beta is the upper bound. Alpha value is the minimum score that the maximizing player is assured of. Beta value is the maximum score that the minimizing player is assured of.

### Score Function

The algorithm above requires a score to be evaluated based on a given state. Our score function only evalulates leaf nodes as follows:

* If leaf is a win: positive score resulting from 22 - number of moves played
* If leaf is a loss: negative score resulting from 22 - number of moves played by opponent
* If leaf is a draw: score is 0

### Implementation

A bitboard is used to represent the state of the board. It maintains the position of the AI and the position of the game. Using a *Bitwise XOR*, we can retrieve the position of the opponent. Other bitwise operations allow the algorithm to determine if a move is valid or if a position is in a draw or winning state.

```
 -  -   -   -   -   -   -
 5  12  19  26  33  40  47
 4  11  18  25  32  39  46
 3  10  17  24  31  38  45
 2  9   16  23  30  37  44
 1  8   15  22  29  36  43
 0  7   14  21  28  35  42
```

The GUI uses **Pygame**  and borrows mouse interactions, board layout, and images from [Four in a Row](http://inventwithpython.com/blog/2011/06/10/new-game-source-code-four-in-a-row/​). 

## Getting Started

The project was completed in *python 3.6* and uses the **Pygame** library

### Install Requirements

1. Activate python virtualenv (Recommended)
2. Install python packages `pip install -r requirements.txt`

### Run 
```python
python3 main.py
```

### How To Play

By default, AI (**BLACK**) will start and place its token. To place your token, drag the **RED** token above the column where you want to place it. Follow the same process until you or the AI wins.

> NOTE: There is a delay (lag) when you place your token. The animations need improvement.

## Code Libraries
- [Four in a Row](http://inventwithpython.com/blog/2011/06/10/new-game-source-code-four-in-a-row/​)
- [Pygame](https://www.pygame.org/)

## Authors
- [Jonathan De Leon](https://www.github.com/JonathanDeLeon)
- [Ethan Beaver](https://www.github.com/ethanbeaver)