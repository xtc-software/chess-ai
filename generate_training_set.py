#!/usr/bin/python3.11
import os
import chess.pgn
import numpy as np
from state import State
import chess.engine

time_limit = chess.engine.Limit(time=0.05)
stockfish_path = "/home/boop/stockfish/stockfish-ubuntu-x86-64-avx2"
depth_limit = 20

def get_dataset(num_samples=None):
    X, Y = [], []
    gn = 0
    # trimdata.pgn
    pgn = open("./data/trimdata50k.pgn")
    while 1:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        board = game.board()
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            for _, move in enumerate(game.mainline_moves()):
                board.push(move)
                info = engine.analyse(board, limit=chess.engine.Limit(depth=depth_limit))
                ser = State(board).serialize()
                X.append(ser)
                Y.append(info["score"].relative.score() / 100)
                
                print(Y[-1]) #! need to update with eval after move
        
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
