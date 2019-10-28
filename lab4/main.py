import tkinter
import abc
import uuid
import random
import time
import math


def random_color():
    return "#{:06x}".format(random.randrange(0, 1 << 24))


class IObject:
    def __init__(self, game):
        self.uuid = uuid.uuid4()
        self.game = game
        game.objects[self.uuid] = self

    def tick(self):
        pass

    @property
    def destroyed(self):
        return False


class IRenderable(IObject, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self):
        pass

    def render_debug(self):
        pass


class NotImplementedError(RuntimeError):
    pass


class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, other):
        if isinstance(other, Vector2d):
            self.x += other.x
            self.y += other.y
            return self
        else:
            raise TypeError("Only vector can be added to vector")

    def __add__(self, other):
        if isinstance(other, Vector2d):
            s = Vector2d(self.x, self.y)
            s.x += other.x
            s.y += other.y
            return s
        else:
            raise TypeError("Only vector can be added to vector")

    def __mul__(self, other):
        s = Vector2d(self.x, self.y)
        s.x *= other
        s.y *= other
        return s

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __isub__(self, other):
        if isinstance(other, Vector2d):
            self.x -= other.x
            self.y -= other.y
            return self
        else:
            raise TypeError("Only vector can be added to vector")

    def __sub__(self, other):
        if isinstance(other, Vector2d):
            s = Vector2d(self.x, self.y)
            s.x -= other.x
            s.y -= other.y
            return s
        else:
            raise TypeError("Only vector can be added to vector")

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)


class IIntersectable(IObject, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def contains(self, point: Vector2d):
        pass

    @abc.abstractmethod
    def intersect(self, other):
        pass


class IClickable(IObject):
    def clicked(self):
        pass


class FrameStats(IRenderable):
    def render(self):
        pass

    def render_debug(self):
        duration = self.game.tick_stamp - self.game.last_tick_stamp
        text = "Tick duration: {0} ms\nFPS: {1}".format(
            int(1000 * duration), int(1.0 / duration))

        self.game.next_frame_canvas.create_text(
            650, 50, text=text, font=(
                "Arial", 20), justify=tkinter.RIGHT)


class Ball(IRenderable, IIntersectable, IClickable):
    def __init__(self, game, position: Vector2d, radius: float):
        self.position = position
        self.radius = radius
        self.color = random_color()
        self._destroyed = False

        self.velocity = Vector2d(
            random.randrange(-50, 50), random.randrange(-50, 50))
        super().__init__(game)

    def render(self):
        self.game.next_frame_canvas.create_oval(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.position.x + self.radius,
            self.position.y + self.radius,
            fill=self.color,
            width=0)

    def render_debug(self):
        self.game.next_frame_canvas.create_oval(
            self.position.x - 2,
            self.position.y - 2,
            self.position.x + 2,
            self.position.y + 2,
            fill='black',
            width=0)
        self.game.next_frame_canvas.create_text(
            self.position.x,
            self.position.y + 15,
            text=str(
                self.uuid).split('-')[0],
            fill='black')

        vel_base = self.position + self.velocity * \
            self.radius * (1 / abs(self.velocity))
        self.game.next_frame_canvas.create_line(
            vel_base.x,
            vel_base.y,
            vel_base.x +
            self.velocity.x,
            vel_base.y +
            self.velocity.y,
            width='3')

    def contains(self, point: Vector2d):
        return self.radius > abs(
            complex(
                self.position.x -
                point.x,
                self.position.y -
                point.y))

    def intersect(self, other):
        if isinstance(other, Ball):
            s = self.position - other.position
            return abs(s) < self.radius + other.radius

    @property
    def destroyed(self):
        return self._destroyed

    def tick(self):
        self.position += self.velocity * 0.02

        if self.position.x + self.radius > self.game.maxw:
            self.velocity.x *= -1
            self.position.x = self.game.maxw - self.radius

        if self.position.y + self.radius > self.game.maxh:
            self.velocity.y *= -1
            self.position.y = self.game.maxh - self.radius

        if self.position.x - self.radius < 0:
            self.velocity.x *= -1
            self.position.x = self.radius

        if self.position.y - self.radius < 0:
            self.velocity.y *= -1
            self.position.y = self.radius

    def clicked(self):
        print("Clicked ball {0}".format(str(self.uuid)))
        self.position.x = random.randrange(100, 700)
        self.position.y = random.randrange(100, 600)
        self.velocity = Vector2d(
            random.randrange(-50, 50), random.randrange(-50, 50))


class BallFactory:
    def __init__(self, game):
        self.game = game

    def intersect(self, ball: Ball):
        for v in self.game.objects.values():
            if v == ball:
                continue
            if isinstance(v, IIntersectable):
                if ball.intersect(v):
                    return True
        return False

    def create_random_ball(self):
        radius = random.randrange(10, 50)
        position = Vector2d(
            random.randrange(
                100, 700), random.randrange(
                100, 500))
        ball = Ball(self.game, position, radius)
        while self.intersect(ball):
            ball.position.x = random.randrange(100, 700)
            ball.position.y = random.randrange(100, 500)
        self.game.objects[ball.uuid] = ball
        return ball

    def set_random_pos(self, old: Ball):
        old.position.x = random.randrange(100, 700)
        old.position.y = random.randrange(100, 500)
        while self.intersect(old):
            old.position.x = random.randrange(100, 700)
            old.position.y = random.randrange(100, 500)


class Game:
    def __init__(self, debug=False):
        self.root = tkinter.Tk()
        self.root.geometry('800x600')

        self._frames = [tkinter.Canvas(self.root, bg='white')]
        self._frame_index = 0

        self.frame_canvas.pack(fill=tkinter.BOTH, expand=1)

        self.objects = {}

        self.debug = debug
        self.pause = False

        self.maxh, self.maxw = 600, 800

        self.last_tick_stamp = time.time()
        self.tick_stamp = time.time()

        ctr = FrameStats(self)
        self.objects[ctr.uuid] = ctr

        self._factory = BallFactory(self)
        self.g = Vector2d(0, 1)

        self.cos = math.cos(0.01)
        self.sin = math.sin(0.01)

    def sanitize_frame_index(self, index=None):
        if index is None:
            index = self._frame_index
        return index % len(self._frames)

    @property
    def frame_canvas(self):
        return self._frames[self._frame_index]

    @property
    def next_frame_canvas(self):
        return self._frames[self.sanitize_frame_index(self._frame_index)]

    def switch_frame(self):
        # self.frame_canvas.pack_forget()
        self.frame_canvas.delete(tkinter.ALL)
        self._frame_index += 1
        self._frame_index = self.sanitize_frame_index()
        # self.frame_canvas.pack(fill=tkinter.BOTH, expand=1)

    def tick(self):
        self.switch_frame()

        self.tick_stamp = time.time()
        d = []

        old_x = self.g.x
        self.g.x = old_x * self.cos - self.g.y * self.sin
        self.g.y = old_x * self.sin + self.g.y * self.cos

        if not self.pause:
            for key in self.objects:
                obj = self.objects[key]
                d.append(obj)
                for key1 in self.objects:
                    obj1 = self.objects[key1]
                    if obj1 in d:
                        continue
                    if isinstance(
                            obj, IIntersectable) and isinstance(
                            obj1, IIntersectable):
                        if obj.intersect(obj1):
                            obj.velocity *= -1
                            obj1.velocity *= -1
                            obj.position += obj.velocity * 0.02
                            obj1.position += obj1.velocity * 0.02
                if isinstance(obj, Ball):
                    obj.velocity += self.g
                obj.tick()

        for key in self.objects:
            if self.objects[key].destroyed:
                del self.objects[key]

        for key in self.objects:
            obj = self.objects[key]
            if isinstance(obj, IRenderable):
                obj.render()
                if self.debug:
                    obj.render_debug()

        self.last_tick_stamp = self.tick_stamp
        self.root.after(17, self.tick)

    def clicked(self, event):
        point = Vector2d(event.x, event.y)
        for key in self.objects:
            obj = self.objects[key]
            if isinstance(
                    obj, IIntersectable) and isinstance(
                    obj, IClickable) and obj.contains(point):
                self._factory.set_random_pos(obj)
                return

    def toggle_pause(self, *args):
        self.pause = not self.pause

    def toggle_debug(self, *args):
        self.debug = not self.debug

    def run(self):
        for i in range(5):
            self._factory.create_random_ball()

        self.root.bind('<Button-1>', self.clicked)
        self.root.bind('<space>', self.toggle_pause)
        self.root.bind('<d>', self.toggle_debug)
        self.root.after(10, self.tick)
        self.root.mainloop()


if __name__ == '__main__':
    game = Game(debug=True)
    game.run()