import tkinter as tk
import random as rnd

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
    
    def create_mount(self):
        self.x1 = rnd.randint(1000, 2000)
        self.y1 = 2000
        self.x2 = rnd.randint(self.x1,2000)
        self.y2 = 2000
        self.x3 = rnd.randint(self.x1,self.x2)
        self.y3 = rnd.randint(500, 2000)
        self.game.objects.append(self.game.canv.create_polygon(self.x1,self.y1,self.x2,self.y2,self.x3,self.y3,fill='black',width=0))
        
        
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
        print(self.camera.vy)
        for obj in self.objects:
            coords = self.canv.coords(obj)
            new_coords = []
            for i in range(0,len(coords)):
                if i%2==0:
                    new_coords.append(coords[i] - self.camera.vx)
                else:
                    new_coords.append(coords[i] - self.camera.vy)
            self.canv.coords(obj, new_coords)
                
        self.root.after(10, self.tick)


    def run(self):
        mounts = Mount(self)
        for i in range(0,3):
            mounts.create_mount()
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
