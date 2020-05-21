# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Form, Button
clr.AddReference('System.Drawing')
from System.Drawing import Size, Point


class Model():
    def __init__(self):
        self._data = "data from model"

    def print_data(self, sender, args):
        print(self._data)


class View(Form):
    def __init__(self):
        self.Size = Size(150, 100)
        self._button = Button()
        self._button.Text = 'Кнопка'
        self._button.Parent = self
        self._button.Location = Point(30, 20)
        self.CenterToScreen()

    def delegate_button_click(self, method):
        self._button.Click += method


class Presenter():
    def __init__(self, form, model):
        form.delegate_button_click(model.print_data)


view = View()
model = Model()
presenter = Presenter(view, model)
view.ShowDialog()
