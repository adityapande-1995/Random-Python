#!python3
# Gameplay module
import numpy as np
import random, os, sys

class Game:
    def __init__(self,n=4):
        self.n = n
        self.board = np.zeros((n,n))
        for p in random.choices(self.empty_slots(), k = 2):
            self.board[p[0], p[1]] = 2
        
        self.update_score()

    def empty_slots(self): # Returns a list of empty squares on the board
        empty_places = []
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i,j] == 0:
                    empty_places.append((i,j))

        return empty_places
    
    def update_score(self):
        self.score = np.sum(self.board)

    def remove_zeros(self,a):
        b = []
        for i in range(len(a)): # Remove zeroes
            if a[i] != 0:
                b.append(a[i])
        
        return b
    
    def list_move(self,a): # Swipe left on a list
        to_merge = 0
        while 1:
            # print(to_merge, a)
            a = self.remove_zeros(a)
            # print(a)
            try:
                if a[to_merge] == a[to_merge + 1]:
                    a[to_merge] = a[to_merge]*2
                    a[to_merge + 1] = 0
            except:
                break
            
            to_merge += 1
        
        # Add trailing zeros
        while len(a) != self.n:
            a.append(0)
        
        return a

    def move_left(self):
        if len(self.empty_slots()) != 0:
            for i in range(self.n):
                self.board[i,:] = self.list_move( self.board[i,:] )
        
            # Insert 2 at a random place
            for p in random.choices(self.empty_slots(), k = 1): 
                self.board[p[0], p[1]] = 2
        
            self.update_score()

    def move_right(self):
        if len(self.empty_slots()) != 0:
            h_mirror = np.flip(self.board,1)
            for i in range(self.n):
                h_mirror[i,:] = self.list_move( h_mirror[i,:] )
        
            self.board = np.flip(h_mirror, 1)
        
            # Insert 2 at a random place
            for p in random.choices(self.empty_slots(), k = 1): 
                self.board[p[0], p[1]] = 2
        
            self.update_score()
    
    def move_up(self):
        if len(self.empty_slots()) != 0:
            for i in range(self.n):
                self.board[:,i] = self.list_move( self.board[:,i] )
        
            # Insert 2 at a random place
            for p in random.choices(self.empty_slots(), k = 1): 
                self.board[p[0], p[1]] = 2
        
            self.update_score()
    
    def move_down(self):
        if len(self.empty_slots()) != 0:
            h_mirror = np.flip(self.board,0)
            for i in range(self.n):
                h_mirror[:,i] = self.list_move( h_mirror[:,i] )
        
            self.board = np.flip(h_mirror, 0)
            # Insert 2 at a random place
            for p in random.choices(self.empty_slots(), k = 1): 
                self.board[p[0], p[1]] = 2
        
            self.update_score()

    def board_show(self):
        for i in range(self.n): # For each row
            L = self.board[i,:].astype(int).tolist()
            for i in range(len(L)):
                if L[i] == 0:
                    L[i] = "-"

            Lc = [str(item).rjust(5,' ') for item in L]
            print(*Lc)
    
    # Play manual game using this method !
    def play_manual(self):
        os.system("clear")
        while 1:
            prev = np.copy(self.board)
            m = input("* Enter w,a,s or d: ")
            if m == 'w': self.move_up()
            elif m == 's': self.move_down()
            elif m == 'a': self.move_left()
            elif m == 'd': self.move_right()
            else : self.move_right()
            os.system("clear")
            print(" *** 2048 clone *** ")
            self.board_show()
            if np.array_equal(prev, self.board):
                print("Game over !")
                sys.exit(0)
            else:
                print("\n", "Score : ", self.score)
            print("-----------------------------------")
    
    # RL agent API !
    def gen_state(self):
        state = np.zeros((1,self.n*self.n))
        M = np.max(self.board)
        z = -1
        for i in range(self.n):
            for j in range(self.n):
                z += 1
                state[0,z] = np.log2(self.board[i,j] + 1)/np.log2(M)
        
        return state

    def reset(self):
        self.board = np.zeros((self.n,self.n))
        for p in random.choices(self.empty_slots(), k = 2):
            self.board[p[0], p[1]] = 2
        
        self.update_score()
        state = self.gen_state()
        return state

    def step(self,action): # Action will be 0 ,1 ,2, or 3
        prev = np.copy(self.board)

        if action == 0: self.move_up()
        elif action == 1: self.move_down()
        elif action == 2: self.move_left()
        elif action == 3: self.move_right()

        done = np.array_equal(prev, self.board)
        next_state = self.gen_state()
        reward = np.max(self.board) + ( self.n**2 - np.count_nonzero(self.board) )*20
        
        return next_state, reward, done, 10
            

if __name__ == '__main__':
    a = Game()
    a.play_manual()
