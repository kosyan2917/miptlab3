import tkinter as t
import random
import time


class Object:
    def __init__(self):
        pass
    def create(self, figure):
        if figure == 'ball':
            canv.delete(t.ALL)
            ball = Ball()
            canv.create_oval(ball.x, ball.x,ball.y,ball.y, fill = ball.color)
            root.after(10, lambda: ball.create('ball'))
class Figure(Object):
    colors = ['black', 'purple', 'yellow','blue', 'red']
    def __init__(self):
        pass
class Ball(Figure):
    def __init__(self):
        self.x = random.randrange(0,800)
        self.y = random.randrange(0,600)
        self.color = random.choice(self.colors)
        
 
    
root = t.Tk()
root.geometry('800x600')
canv = t.Canvas(root, bg='white')
canv.pack(fill=t.BOTH, expand=1)

Ball().create('ball')  

root.mainloop()
