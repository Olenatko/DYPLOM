from random import random
import math

class CPN:
    def __init__(self, x, kohonen, y, weights_file=None):
        self.x = x
        self.kohonen = kohonen
        self.y = y
        self.eta1 = 0.7
        self.eta2 = 0.5
        self.make_neurons()
        self.make_weights()
        self.kohonen_justice = list(0 for i in range(0, kohonen))

    def rand(self, a, b):
        return a + (b-a)*random()
    def make_neurons(self):
        self.neurons = []
        for i in range(0, 3):
            self.neurons.append([])
        for i in range(0, self.x):
            self.neurons[0].append(0)
        for i in range(0, self.kohonen):
            self.neurons[1].append(0)
        for i in range(0, self.y):
            self.neurons[2].append(0)
        return self.neurons

    def make_weights(self):
        self.weights = []
        for i in range(0, 2):
            self.weights.append([])
        for i in range(0, self.kohonen):
            self.weights[0].append([])
            for j in range(0, self.x):
                self.weights[0][i].append(self.rand(0,50)) #self.random(0,50)
        for i in range(0, self.y):
            self.weights[1].append([])
            for j in range(0, self.kohonen):
                self.weights[1][i].append(self.rand(0,50)) # random()
        return self.weights


    def euclidean_distance(self, weights):
        euclid = 0
        for i in range(0, self.x):
            euclid += (self.neurons[0][i] - self.weights[0][weights][i]) ** 2
        return math.sqrt(euclid)

    def find_winner(self):
        self.max_index = 0
        max_value = None
        previous_value = 0
        previous_index = 0
        for i in range(0, self.kohonen):
            euclid = self.euclidean_distance(i)
            if max_value is None:
                max_value = euclid
            if euclid < max_value:
                previous_value = max_value
                previous_index = self.max_index
                max_value = euclid

                self.max_index = i
        print("нейрончик номер", self.max_index)

    def set_winner(self):
        for i in range(0, self.kohonen):
            self.neurons[1][i] = 0
        self.neurons[1][self.max_index] = 1

    def calc_output(self):
        for i in range(0, self.y):
            self.neurons[2][i] = sum(self.weights[1][i][x]*self.neurons[1][x] for x in range(0, self.kohonen))

    def kohonen_formula(self, x_i):
        return self.eta1*(self.neurons[0][x_i]-self.weights[0][self.max_index][x_i])

    def grossberg_formula(self, kohonen_index, y):

        result = self.eta2*(self.neurons[0][y] - self.neurons[2][y])*self.neurons[1][kohonen_index]
        return result

    def set_input(self, x):
        self.neurons[0] = x

    def learn(self):
        self.propagate()
        self.find_winner()
        for cycle in range(0, 100):
            for i in range(0, self.x):
                self.weights[0][self.max_index][i] += self.kohonen_formula(i)

        self.set_winner()
        for cycle in range(0, 100):
            for i in range(0, self.y):
                for j in range(0, self.kohonen):
                    self.weights[1][i][j] += self.grossberg_formula(j, i)
            self.calc_output()


    def propagate(self):
        self.find_winner()
        self.set_winner()
        self.calc_output()


    def get_output(self):
        return self.neurons[2]
