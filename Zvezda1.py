import tkinter as tk
import random as rnd


class Players:
    def __init__(self, game):
        self.game = game
        self.x = 525
        self.vx = 0

    def move_forward(self):
        self.vx = 2

    def move_backward(self):
        self.vx = -2

    def create_player1(self):
        self.obj = [self.game.objects.append(self.game.canv.create_oval(500, 2000, 520, 1980, fill='black')), self.game.objects.append(self.game.canv.create_oval(530, 2000, 550, 1980, fill='black')), self.game.objects.append(self.game.canv.create_rectangle(500, 1985, 550, 1970, fill='red'))]
        pass

class Camera:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 1280
        self.y2 = 720
        self.vx = 0
        self.vy = 0
    def set_x_speedmore(self, event):
        self.vx+=2
    
    def set_y_speedmore(self, event):
        self.vy+=2

    def set_x_speedless(self, event):
        self.vx-=2
        
    def set_y_speedless(self, event):
        self.vy-=2


class Mount:
    def __init__(self, Game):
        self.game = Game
        self.x1 = rnd.randint(1000, 2000)
        self.y1 = 2000
        self.x2 = rnd.randint(self.x1, 2000)
        self.y2 = 2000
        self.x3 = rnd.randint(self.x1, self.x2)
        self.y3 = rnd.randint(500, 2000)
        self.obj = self.game.canv.create_polygon(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, fill='black',
                                                 width=0)


class Game:
    def __init__(self, camera):
        self.camera = camera
        self.objects = []
        self.root = tk.Tk()
        self.fr = tk.Frame(self.root)
        self.root.geometry('1280x720')
        self.canv = tk.Canvas(self.root, bg='white')
        self.canv.pack(fill=tk.BOTH, expand=1)

    def tick(self):
        print([self.camera.x1,self.camera.x2,self.camera.y1,self.camera.y2])
        self.camera.x1 += self.camera.vx
        self.camera.x2 += self.camera.vx
        self.camera.y1 += self.camera.vy
        self.camera.y2 += self.camera.vy
        if self.camera.x1 < 0:
            self.camera.x1 = 0
            self.camera.x2 = 1280
            self.camera.vx = 0
        if self.camera.x2 > 3000:
            self.camera.vx = 0
            self.camera.x2 = 3000
            self.camera.x1 = 1720
        if self.camera.y1 < 0:
            self.camera.vy = 0
            self.camera.y2 = 720
            self.camera.y1 = 0
        if self.camera.y2 > 2000:
            self.camera.vy = 0
            self.camera.y1 = 1280
            self.camera.y2 = 2000
        for object in self.objects:
            coords = self.canv.coords(object.obj)
            new_coords = []
            for i in range(0,len(coords)):
                if i%2==0:
                    new_coords.append(coords[i] - self.camera.vx)
                else:
                    new_coords.append(coords[i] - self.camera.vy)
            self.canv.coords(object.obj, new_coords)

        self.root.after(10, self.tick)

    def run(self):
        #self.objects.append(self.canv.create_line(0, 0, 3000, 0))
        #self.objects.append(self.canv.create_line(3000, 0, 3000, 2000))
        #self.objects.append(self.canv.create_line(0, 0, 100, 50))
        player1 = Players(self)
        player2 = Players(self)
        player1.create_player1()
        for i in range(0,20):
            self.objects.append(Mount(self))
        print(self.objects)
        self.root.bind('<Down>', self.camera.set_y_speedmore)
        self.root.bind('<Up>', self.camera.set_y_speedless)
        self.root.bind('<Right>', self.camera.set_x_speedmore)
        self.root.bind('<Left>', self.camera.set_x_speedless)
        self.root.after(10, self.tick)
        self.root.mainloop()


if __name__ == '__main__':
    game = Game(Camera())
    game.run()
