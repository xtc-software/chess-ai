#! /usr/bin/python3.11
import torch
from state import State
from train import Net
import chess

class Evaluater():
    def __init__(self):
        vals = torch.load("nets/value.pth", map_location=lambda storage, loc:storage)
        self.model = Net()
        self.model.load_state_dict(vals)
    
    def __call__(self, s):
        board = s.serialize()[None]
        board = s.serialize()[None]
        output = self.model(torch.tensor(board).float())
        
        return float(output.data[0][0])
        

def exploreTree(e,s):
    out = []
    for move in s.edges():
        s.board.push(move)
        out.append((move, e(s)))
        s.board.pop()
    
    return out
        
if __name__ == "__main__":
    e = Evaluater()
    s = State()

    while not s.board.is_game_over():
        moveList = sorted(exploreTree(e,s), key= lambda x: x[1], reverse=s.board.turn)
        s.board.push(moveList[0][0])

    print(s.board.result())