import tkinter as t
import random
import time
import numpy as np 


class Object:

    def __init__(self):
        pass

    def rpd(self):
        self.x += self.vx
        self.y += self.vy
        canv.delete(self.obj)
        self.obj = canv.create_oval(self.x, self.y, self.x + 2 * self.r, 
                                    self.y + 2 * self.r, fill = self.color)
        root.after(100, self.rpd)
        
        


    def create(self, figure):
        if figure == 'ball':
            canv.delete(t.ALL)
            ball = Ball()
            self.obj = canv.create_oval(ball.x, ball.y, ball.x + 2 * ball.r, 
                                        ball.y + 2 * ball.r, fill = ball.color)
            root.after(1000, lambda ball = ball: ball.create('ball'))
            self.rpd


class Figure(Object):

    colors = ['black', 'purple', 'yellow','blue', 'red']
    def __init__(self):
        pass


class Ball(Figure):

    def __init__(self):
        self.x = random.randrange(75, 600)
        self.y = random.randrange(75, 600)
        self.r = random.randrange(30, 150)
        self.vx = random.randrange(-5, 5)
        self.vy = random.randrange(-5, 5)
        self.color = random.choice(self.colors)


class NewObject(Object):
    stateArray = np.array([[0, 0], [0, 0]], float) 
    def __init__(self, pStateArray):
        self.stateArray = pStateArray
        pass


### 17:54 create new instace of object with state array for coords and delta cords 

root = t.Tk()
root.geometry('800x600')
canv = t.Canvas(root, bg='white')
canv.pack(fill = t.BOTH, expand = 1)

def click(event):
    print(event.x, event.y)

canv.bind('<Button-1>', click)

Ball().create('ball')  

root.mainloop()