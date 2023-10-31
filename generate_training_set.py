#!/usr/bin/python3.11
import os
import chess.pgn
import numpy as np
from state import State
import chess.engine

time_limit = chess.engine.Limit(time=0.05)
stockfish_path = "/home/boop/stockfish/stockfish-ubuntu-x86-64-avx2"
depth_limit = 10
engine_config = {
    "Threads": 4,  # Adjust to the number of CPU cores available
    "Hash": 4096,  # Adjust based on available RAM (in MB)
}


def get_dataset(num_samples=None):
    X, Y = [], []
    gn = 0
    # trimdata.pgn
    pgn = open("./data/trimdata50k.pgn")
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        for key, value in engine_config.items():
            engine.configure({key: value})
        
        while 1:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            board = game.board()
            for _, move in enumerate(game.mainline_moves()):
                board.push(move)
                info = engine.analyse(board, limit=chess.engine.Limit(depth=depth_limit))
                ser = State(board).serialize()
                val = 0
                if info and info["score"] is not None:
                    if info["score"].is_mate() and info["score"].white:
                        val = 1000
                    elif info["score"].is_mate() and info["score"].black:
                        val = -1000
                    else:
                        val = info["score"].relative.score() / 100
                    
                    X.append(ser)
                    Y.append(val)
                else:
                    continue
            
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
