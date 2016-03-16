from smartass import *
import matplotlib.pyplot as plt
from math import *
Network = CPN(100, 3, 100)

def make_points(function, a, b):
    x = []
    y = []
    func = lambda x: eval(function)
    for i in range(a, b):
        x.append(i)
        y.append(func(i))
    Network.set_input(x+y)
    Network.learn()

    x_learned = []
    y_learned = []
    learned = []
    for i in range(a, b):
        x_learned.append(i)
        y_learned.append(0)
    Network.set_input(x_learned + y_learned)
    Network.propagate()
    learned = Network.get_output()

    x_v = int(len(learned)/2)

    plt.plot(x, y)
    plt.plot(learned[:x_v], learned[x_v:], "ro")
    plt.show()

def check(function, a, b):
    x = []
    y = []
    func = lambda x: eval(function)
    for i in range(a, b):
        x.append(i)
        y.append(func(i))

    x_learned = []
    y_learned = []
    learned = []
    for i in range(a, b):
        x_learned.append(0)
        y_learned.append(func(i))
    Network.set_input(x_learned + y_learned)
    Network.propagate()
    learned = Network.get_output()

    x_v = int(len(learned)/2)

    plt.plot(x, y)
    plt.plot(learned[:x_v], learned[x_v:])

    plt.show()




make_points("sin(x)", 0, 50)
make_points("x*x", 0, 50)
check("x*x", 0, 50)
check("sin(x)", 0, 50)
