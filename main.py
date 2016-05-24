from smartass import *
import matplotlib.pyplot as plt
from math import *
from tkinter import *
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(Frame):
    def __init__(self, master=None):
        master.title("Мережа зустрічного поширення")
        Frame.__init__(self, master)
        self.Network = CPN(100, 2, 100)
        self.grid()
        self.createWidgets()


    def createWidgets(self):
        self.function_label = Label(self)
        self.function_label["text"] = "Задати функцію"
        self.function_label.grid(row=0, column=0)

        self.function_combo = Combobox(self)
        self.function_combo["values"] = ["x*x", "cos(x)"]
        self.function_combo.set("x*x")
        self.function_combo.grid(row=0, column=1)

        self.a_label = Label(self)
        self.a_label["text"] = "Задати ліву межу"
        self.a_label.grid(row=1, column=0)

        self.a = Entry(self)
        self.a.insert(END, '0')
        self.a.grid(row=1, column=1)

        self.b_label = Label(self)
        self.b_label["text"] = "Задати праву межу"
        self.b_label.grid(row=2, column=0)

        self.b = Entry(self)
        self.b.insert(END, '50')
        self.b.grid(row=2, column=1)

        self.learning_button = Button(self)
        self.learning_button["text"] = "Навчити"
        self.learning_button["command"] = self.make_points
        self.learning_button.grid(row=3, column=0)

        self.check_button = Button(self)
        self.check_button["text"] = "Розпізнати"
        self.check_button["command"] = self.check
        self.check_button.grid(row=3, column=1)

        self.learn_canvas = Canvas(self)
        self.learn_canvas.grid(row=4, column=0)

        self.check_canvas = Canvas(self)
        self.check_canvas.grid(row=4, column=1)


    def make_points(self):
        function = self.function_combo.get()
        a = int(self.a.get())
        b = int(self.b.get())
        x = []
        y = []
        func = lambda x: eval(function)
        for i in range(a, b):
            x.append(i)
            y.append(func(i))
        self.Network.set_input(x+y)
        self.Network.learn()

        x_learned = []
        y_learned = []
        learned = []
        for i in range(a, b):
            x_learned.append(0)
            y_learned.append(func(i))
        self.Network.set_input(x_learned + y_learned)
        self.Network.propagate()
        learned = self.Network.get_output()

        x_v = int(len(learned)/2)
        f = Figure()
        a = f.add_subplot(111)
        a.plot(x, y, '--bo')

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(row=4, column=0)

        f = Figure()
        b = f.add_subplot(111)

        b.plot(learned[:x_v], learned[x_v:], '--bo')
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(row=4, column=1)


    def check(self):
        function = self.function_combo.get()
        a = int(self.a.get())
        b = int(self.b.get())
        x = []
        y = []
        func = lambda x: eval(function)
        x_test = []
        y_test = []
        counter = 0
        for i in range(a, b):
            counter += 1
            if counter % 5 == 0:
                counter = 0
                x.append(i)
                y.append(func(i))
                x_test.append(i)
                y_test.append(func(i))
            else:
                x.append(0)
                y.append(0)

        x_learned = []
        y_learned = []
        learned = []
        for i in range(a, b):
            x_learned.append(0)
            y_learned.append(func(i))
        self.Network.set_input(x_learned + y_learned)
        self.Network.propagate()
        learned = self.Network.get_output()

        x_v = int(len(learned) / 2)

        f = Figure()
        a = f.add_subplot(111)
        a.plot(x_test, y_test, '--bo')

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(row=4, column=0)

        f = Figure()
        a = f.add_subplot(111)
        a.plot(learned[x_v:], learned[:x_v], '--bo')

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(row=4, column=1)




root = Tk()
app = Application(master=root)
app.mainloop()
