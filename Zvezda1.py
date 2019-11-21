import tkinter as tk
import random as rnd
import math


class Players:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.vx = 0
        self.power = 50
        self.on = 0
        self.an = math.pi/2
        self.van = 0

    def targetting(self, event):
        print(event.keycode)
        if event.keycode == 111:
            self.van = math.pi/256
        if event.keycode == 116:
            self.van = -math.pi/256
        print(self.game.canv.coords(self.obj[3]))

    def fire_start(self, event):
        self.on = 1
        self.vx = 0.1

    def fire_end(self, event):
        self.on = 0
        self.bullet = Bullet(self.game)
        self.game.objects.append(self.bullet)
        #print(self.bullet)
        self.bullet.shot(self.gun[2], self.gun[3], self.power, self.an)
        self.game.root.unbind('<space>')
        self.game.root.unbind('<KeyRelease-space>')

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
        self.gun = self.game.canv.coords(self.obj[3])
        if self.on:
            self.game.canv.itemconfig(self.obj[3], fill='orange')
            if self.power < 200:
                self.power += 0.5
        else:
            self.game.canv.itemconfig(self.obj[3], fill='black')
            self.power = 50
        self.x += self.vx
        self.an += self.van
        self.game.canv.coords(self.obj[3], self.gun[0], self.gun[1], self.gun[0] + self.power * math.cos(self.an),
                              self.gun[1] + self.power * math.sin(self.an) * (-1))
        #print(self.game.canv.coords(self.obj[3]))
        print(self.van)
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
        self.van = 0


class Bullet:
    def __init__(self, game):
        self.x = 0
        self.y = 0
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.an = 0
        self.game = game
        self.acc = 0.05
        self.module = 0.1
        self.x0 = 0
        self.y0 = 0
        self.obj = 0
        self.timer = 1000
        self.time = 0

    def shot(self, x, y, power, an):
        self.obj = self.game.canv.create_oval(x-self.r, y-self.r, x+self.r, y+self.r, fill='blue')
        self.x = x
        self.y = y
        self.an = an
        self.vx = power * math.cos(self.an) * self.module
        self.vy = power * (-1) * math.sin(self.an) * self.module

    def render(self):
        #print(self.game.camera.vx, self.game.camera.vy)
        if self.time < self.timer:
            self.x += self.vx
            self.y += self.vy
            self.game.canv.coords(self.obj, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)
            self.time += 1
        else:
            pass
        self.vy += self.acc

            


class Camera:
    def __init__(self, game):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 1280
        self.y2 = 720
        self.vx = 0
        self.vy = 0
        self.game = game

    def set_x_speedmore(self, event):
        self.vx = 4
    
    def set_y_speedmore(self, v, event):
        self.vy = v

    def set_x_speedless(self, v, event):
        self.vx = v
        
    def set_y_speedless(self, v, event):
        self.vy = v

    def set_pos(self, x, y):
        diffx = self.x2 - x
        diffy = self.y2 - y
        for gameobj in self.game.objects:
            coords = self.game.canv.coords(gameobj.obj)
            if isinstance(gameobj, Players):
                for j in range(0, len(gameobj.obj)):
                    coords = self.game.canv.coords(gameobj.obj[j])
                    new_coords = []
                    for i in range(0, len(coords)):
                        if i % 2 == 0:
                            new_coords.append(coords[i] + diffx)
                        else:
                            new_coords.append(coords[i] + diffy)
                    self.game.canv.coords(gameobj.obj[j], new_coords)
                gameobj.render()
            else:
                new_coords = []
                coords = self.game.canv.coords(gameobj.obj)
                for i in range(0,len(coords)):
                    if i%2==0:
                        new_coords.append(coords[i] + diffx)
                    else:
                        new_coords.append(coords[i] + diffy)
                self.game.canv.coords(gameobj.obj, new_coords)
                if isinstance(gameobj, Bullet):
                    gameobj.render()
        self.x2 = x
        self.y2 = y
        self.x1 = self.x2 - 1280
        self.y1 = self.y2 - 720


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
    def __init__(self):
        self.turn = 1
        self.camera = Camera(self)
        self.objects = []
        self.root = tk.Tk()
        self.fr = tk.Frame(self.root)
        self.root.geometry('1280x720')
        self.canv = tk.Canvas(self.root, bg='white')
        self.canv.pack(fill=tk.BOTH, expand=1)

    def tick(self):
        #print([self.camera.x1,self.camera.x2,self.camera.y1,self.camera.y2])
        self.camera.set_pos(self.camera.x2 + self.camera.vx, self.camera.y2 + self.camera.vy)
        if self.camera.x1 < 0:
            self.camera.set_pos(1280, self.camera.y2)
            self.vx = 0
        if self.camera.x2 > 3000:
            self.camera.set_pos(3000, self.camera.y2)
            self.vx = 0
        if self.camera.y1 < 0:
            self.camera.set_pos(self.camera.x2, 720)
            self.vy = 0
        if self.camera.y2 > 2000:
            self.camera.set_pos(self.camera.x2, 2000)
            self.vy = 0

        '''for gameobj in self.objects:
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
                gameobj.render()
            else:
                new_coords = []
                coords = self.canv.coords(gameobj.obj)
                for i in range(0,len(coords)):
                    if i%2==0:
                        new_coords.append(coords[i] - self.camera.vx)
                    else:
                        new_coords.append(coords[i] - self.camera.vy)
                self.canv.coords(gameobj.obj, new_coords)
                if isinstance(gameobj, Bullet):
                    gameobj.render()'''
        self.root.after(10, self.tick)

    def next_turn(self, event):
        self.turn += 1
        print('NExt turn')
        if self.turn % 2 == 0:
            self.player1.vx = 0
            self.root.bind('<Right>', self.player2.move_forward)
            self.root.bind('<Left>', self.player2.move_backward)
            self.root.bind('<KeyRelease-Right>', self.player2.stop)
            self.root.bind('<KeyRelease-Left>', self.player2.stop)
            self.root.bind('<KeyPress>', self.player2.targetting)
            self.root.bind('<space>', self.player2.fire_start)
            self.root.bind('<KeyRelease-space>', self.player2.fire_end)
            self.camera.set_pos(3000, 2000)
        else:
            self.player2.vx = 0
            self.root.bind('<Right>', self.player1.move_forward)
            self.root.bind('<Left>', self.player1.move_backward)
            self.root.bind('<KeyRelease-Right>', self.player1.stop)
            self.root.bind('<KeyRelease-Left>', self.player1.stop)
            self.root.bind('<KeyPress>', self.player1.targetting)
            self.root.bind('<KeyRelease-space>', self.player1.fire_end)
            self.root.bind('<space>', self.player1.fire_start)
            self.camera.set_pos(1280,2000)

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
        #print(self.objects)
        self.root.bind('<Right>', self.player1.move_forward)
        self.root.bind('<Left>', self.player1.move_backward)
        self.root.bind('<KeyRelease-Right>', self.player1.stop)
        self.root.bind('<KeyRelease-Left>', self.player1.stop)
        self.root.bind('<KeyPress>', self.player1.targetting)
        self.root.bind('<space>', self.player1.fire_start)
        self.root.bind('<KeyRelease-space>', self.player1.fire_end)
        self.root.bind('c', self.next_turn)
        self.root.after(10, self.tick)
        self.root.mainloop()


if __name__ == '__main__':
    game = Game()
    game.run()
