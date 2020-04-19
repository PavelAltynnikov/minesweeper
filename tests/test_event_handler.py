# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Form, Button
clr.AddReference('System.Drawing')
from System.Drawing import Size, Point
from abc import abstractmethod

def foo():
    print(123)


a = foo
a()


class Test():
    def __init__(self, function):
        self.b = function

    def function(self):
        print("Я из класса Test")


t = Test(foo)
t.b()


class Test2():
    def __init__(self, another_class):
        self.handler = another_class.function


t2 = Test2(t)
t2.handler()


class Test3():
    def __init__(self, another_class):
        # self.handler_method = another_class.function
        another_class.function = self.handler_method

    def handler_method(self):
        pass

    def handler_method(self):
        print("Я из Test3")


t3 = Test3(t)
# t3.handler_method()
t.function()


class Model():
    pass


class View(Form):
    def __init__(self):
        self.Size = Size(150, 100)
        self._button = Button()
        self._button.Text = 'Кнопка'
        self._button.Parent = self
        self._button.Location = Point(30, 20)
        self.CenterToScreen()

        self.button_start_event_handler = self._button.Click


class Presenter():
    def __init__(self, form, model):
        form.button_start_event_handler += self.function_handler

    def function_handler(self, sender, args):
        print("Я из Presenter")
        print(sender)
        print(args)


view = View()
model = Model()
presenter = Presenter(view, model)
view.ShowDialog()
