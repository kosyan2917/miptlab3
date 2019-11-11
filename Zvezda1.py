import tkinter as tk
import random as rnd
import math


class Players:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.vx = 0
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1

    def targetting(self, event=0):
        print(event.x, event.y)
        if event:
            try:
                self.an = math.atan((event.y - 250) / (event.x - self.x))
            except ZeroDivisionError:
                self.an = math.pi/2
        if self.f2_on:
            self.game.canv.itemconfig(self.obj[3], fill='orange')
        else:
            self.game.canv.itemconfig(self.obj[3], fill='black')
        self.game.canv.coords(self.obj[3], self.x, 690, self.x + 50 * math.cos(self.an), 690 + 50*math.sin(self.an))
        print(self.game.canv.coords(self.obj[3]))

    def move_forward(self, event):
        self.vx = 2

    def move_backward(self, event):
        self.vx = -2

    def stop(self, event):
        self.vx = 0

    def create_player1(self):
        self.x = 525
        self.obj = [self.game.canv.create_oval(500, 2000, 520, 1980, fill='black'), self.game.canv.create_oval(530, 2000, 550, 1980, fill='black'), self.game.canv.create_rectangle(500, 1985, 550, 1970, fill='red'), self.game.canv.create_line(525,1970,525,1920,width=7)]

    def create_player2(self):
        self.x = 2525
        self.obj = [self.game.canv.create_oval(2500, 2000, 2520, 1980, fill='black'), self.game.canv.create_oval(2530, 2000, 2550, 1980, fill='black'), self.game.canv.create_rectangle(2500, 1985, 2550, 1970, fill='red'), self.game.canv.create_line(2525,1970,2525,1920,width=7)]

    def render(self):
        self.x += self.vx
        if (self.x > 975) and (self.x <1000):
            self.vx = 0
            self.x = 975
        elif self.x < 25:
            self.vx = 0
            self.x = 25
        elif (self.x > 2000) and (self.x < 2025):
            self.vx = 0
            self.x = 2025
        elif self.x > 2975:
            self.vx = 0
            self.x = 2975
        for i in range(0, 4):
            cors = self.game.canv.coords(self.obj[i])
            cors[0] += self.vx
            cors[2] += self.vx
            self.game.canv.coords(self.obj[i], cors)


class Camera:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 1280
        self.y2 = 720
        self.vx = 0
        self.vy = 0
    def set_x_speedmore(self, event):
        self.vx = 4
    
    def set_y_speedmore(self, v, event):
        self.vy = v

    def set_x_speedless(self, v, event):
        self.vx = v
        
    def set_y_speedless(self, v, event):
        self.vy = v

    def set_pos(self, x, y):
        for gameobj in self.objects:
            coords = self.canv.coords(gameobj.obj)
            if isinstance(gameobj, Players):
                print(gameobj)
                print(gameobj.obj)
                for j in range(0, len(gameobj.obj)):
                    coords = self.canv.coords(gameobj.obj[j])
                    new_coords = []
                    for i in range(0, len(coords)):
                        if i % 2 == 0:
                            new_coords.append(coords[i] - self.camera.vx)
                        else:
                            new_coords.append(coords[i] - self.camera.vy)
                    self.canv.coords(gameobj.obj[j], new_coords)
            else:
                new_coords = []
                coords = self.canv.coords(gameobj.obj)
                for i in range(0,len(coords)):
                    if i%2==0:
                        new_coords.append(coords[i] - self.camera.vx)
                    else:
                        new_coords.append(coords[i] - self.camera.vy)
                self.canv.coords(gameobj.obj, new_coords)


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
        self.turn = 1
        self.camera = camera
        self.objects = []
        self.root = tk.Tk()
        self.fr = tk.Frame(self.root)
        self.root.geometry('1280x720')
        self.canv = tk.Canvas(self.root, bg='white')
        self.canv.pack(fill=tk.BOTH, expand=1)

    def tick(self):
        #print([self.camera.x1,self.camera.x2,self.camera.y1,self.camera.y2])
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

        for gameobj in self.objects:
            coords = self.canv.coords(gameobj.obj)
            if isinstance(gameobj, Players):
                for j in range(0, len(gameobj.obj)):
                    coords = self.canv.coords(gameobj.obj[j])
                    new_coords = []
                    for i in range(0, len(coords)):
                        if i % 2 == 0:
                            new_coords.append(coords[i] - self.camera.vx)
                        else:
                            new_coords.append(coords[i] - self.camera.vy)
                    self.canv.coords(gameobj.obj[j], new_coords)
            else:
                new_coords = []
                coords = self.canv.coords(gameobj.obj)
                for i in range(0,len(coords)):
                    if i%2==0:
                        new_coords.append(coords[i] - self.camera.vx)
                    else:
                        new_coords.append(coords[i] - self.camera.vy)
                self.canv.coords(gameobj.obj, new_coords)
        self.player1.render()
        self.player2.render()
        self.root.after(10, self.tick)

    def next_turn(self, event):
        self.turn += 1
        if self.turn % 2 == 0:
            self.player1.vx = 0
            self.root.bind('<Right>', self.player2.move_forward)
            self.root.bind('<Left>', self.player2.move_backward)
            self.root.bind('<KeyRelease-Right>', self.player2.stop)
            self.root.bind('<KeyRelease-Left>', self.player2.stop)
            self.root.bind('<Motion>', self.player2.targetting)
            self.camera.vx = 1720
        else:
            self.player2.vx = 0
            self.root.bind('<Right>', self.player1.move_forward)
            self.root.bind('<Left>', self.player1.move_backward)
            self.root.bind('<KeyRelease-Right>', self.player1.stop)
            self.root.bind('<KeyRelease-Left>', self.player1.stop)
            self.root.bind('<Motion>', self.player1.targetting)
            self.camera.vx = -1720

    def run(self):
        self.camera.vy = 1280
        self.player1 = Players(self)
        self.objects.append(self.player1)
        self.player2 = Players(self)
        self.objects.append(self.player2)
        self.player1.create_player1()
        self.player2.create_player2()
        for i in range(0,20):
            self.objects.append(Mount(self))
        print(self.objects)
        self.root.bind('<Right>', self.player1.move_forward)
        self.root.bind('<Left>', self.player1.move_backward)
        self.root.bind('<KeyRelease-Right>', self.player1.stop)
        self.root.bind('<KeyRelease-Left>', self.player1.stop)
        self.root.bind('<KeyPress>', self.player1.targetting)
        self.root.bind('c', self.next_turn)
        self.root.after(10, self.tick)
        self.root.mainloop()


if __name__ == '__main__':
    game = Game(Camera())
    game.run()
