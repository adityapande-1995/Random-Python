#!python3
# Text based rubik's cube game

import numpy as np
import random

class Cube:
    def __init__(self):
        self.state = {}
        self.state['F'] = np.array([[1,1,1], [1,1,1], [1,1,1]])
        self.state['R'] = np.array([[2,2,2], [2,2,2], [2,2,2]])
        self.state['B'] = np.array([[3,3,3], [3,3,3], [3,3,3]])
        self.state['L'] = np.array([[4,4,4], [4,4,4], [4,4,4]])
        self.state['U'] = np.array([[5,5,5], [5,5,5], [5,5,5]])
        self.state['D'] = np.array([[6,6,6], [6,6,6], [6,6,6]])

    def show(self):
        for face, colors in self.state.items():
            print("Face ", face ," :  \n", colors)

    def scramble(self, n=21):
        moves = ['ri', 'ro', 'ui', 'uo', 'li', 'lo','di', 'do']
        for i in range(n):
            self.rotate( random.choice(moves) )

    def rotate(self, move):
        # Right face as centre of axis
        if move == 'ro':
            self.state['F'][:,2], self.state['D'][:,2], self.state['B'][:,2], self.state['U'][:,2] = \
                    self.state['U'][:,2].copy(), self.state['F'][:,2].copy(), self.state['D'][:,2].copy(),\
                    self.state['B'][:,2].copy()

        elif move == 'ri':
            self.state['F'][:,2], self.state['D'][:,2], self.state['B'][:,2], self.state['U'][:,2] = \
                    self.state['D'][:,2].copy(), self.state['B'][:,2].copy(), self.state['U'][:,2].copy(),\
                    self.state['F'][:,2].copy()

        # Left face as centre of axis
        elif move == 'li':
            self.state['F'][:,0], self.state['D'][:,0], self.state['B'][:,0], self.state['U'][:,0] = \
                    self.state['U'][:,0].copy(), self.state['F'][:,0].copy(), self.state['D'][:,0].copy(),\
                    self.state['B'][:,0].copy()

        elif move == 'lo':
            self.state['F'][:,0], self.state['D'][:,0], self.state['B'][:,0], self.state['U'][:,0] = \
                    self.state['D'][:,0].copy(), self.state['B'][:,0].copy(), self.state['U'][:,0].copy(),\
                    self.state['F'][:,0].copy()
        
        # Up face as centre of axis
        elif move == 'uo':
            self.state['F'][0,:], self.state['R'][0,:], self.state['B'][0,:], self.state['L'][0,:] = \
                self.state['L'][0,:].copy(), self.state['F'][0,:].copy(), self.state['R'][0,:].copy(),\
                self.state['B'][0,:].copy()

        elif move == 'ui':
            self.state['F'][0,:], self.state['R'][0,:], self.state['B'][0,:], self.state['L'][0,:] = \
                self.state['R'][0,:].copy(), self.state['B'][0,:].copy(), self.state['L'][0,:].copy(),\
                self.state['F'][0,:].copy()

        # Down face as centre of axis
        elif move == 'do':
            self.state['F'][2,:], self.state['R'][2,:], self.state['B'][2,:], self.state['L'][2,:] = \
                self.state['R'][2,:].copy(), self.state['B'][2,:].copy(), self.state['L'][2,:].copy(),\
                self.state['F'][2,:].copy()

        elif move == 'di':
            self.state['F'][2,:], self.state['R'][2,:], self.state['B'][2,:], self.state['L'][2,:] = \
                self.state['L'][2,:].copy(), self.state['F'][2,:].copy(), self.state['R'][2,:].copy(),\
                self.state['B'][2,:].copy()
        
        else:
            print("Invalid move")


if __name__ == '__main__':
    a = Cube()
    print("Unscrambled cube :")
    a.show() 
    # ro, ri, lo, li, uo, ui, do, di --> available options to rotate 
    a.rotate('ro')
    print("\nScrambled cube :")
    a.scramble()
    a.show()
