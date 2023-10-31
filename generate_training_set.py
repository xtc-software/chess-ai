#!/usr/bin/python3.11
import os
import chess
import numpy as np
from state import State


def get_dataset(num_samples=None):
    X, Y = [], []
    
    # trimdata.pgn
    pgn = open("./data/trimdata.pgn")
    while 1:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        board = game.board()
        for i, move in enumerate(game.mainline_moves()):
            board.push(move)
            ser = State(board).serialize()
            X.append(ser)
            Y.append(move) #! need to update with eval after move
        
        print("parsing game %d, got %d examples" % (gn, len(X)), end='\r')
        if num_samples is not None and len(X) > num_samples:
            return X, Y
        gn += 1
    X = np.array(X)
    Y = np.array(Y)
    return X, Y


if __name__ == "__main__":
    X, Y = get_dataset(None)
    np.savez("processed/dataset_100k.npz", X, Y)
