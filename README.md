## chess engine 
use a neural net to prune a search tree of possible moves 

definition: value network
V = f(state)

V is -1 when black is winning
V is 0 when the state of the board is drawn
V is 1 when white is winning

### Storing the game state
we use a 9x9 array to store the state of the game 
    - 8x8 for the pieces on the board 
    - 4 squares for castling rights for both sides
    - 1 square for who's turn it is
    -  