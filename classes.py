import random


class Cat:
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    def sleep(self, name):
        print("{0} спит".format(self.name))

    def meow(self, name):
        print("{0} орет: МУЦУРАЕВА ХАЧЮ!".format(self.name))

    def get_name(self):
        try:
            print(self.name)
        except AttributeError:
            print("Daite imya koty!")

    def set_name(self, name):
        self.name = name

    def __add__(self, name):
        pass


a = [Cat(), Cat(), Cat(), Cat()]
b = 1
for i in a:
    i.set_name('Номер {0}'.format(b))
    b += 1
    i.get_name()

for i in range(0, 5):
    b = random.randint(0, 2)
    c = a[random.randint(0, 3)]
    if b == 0:
        pass
