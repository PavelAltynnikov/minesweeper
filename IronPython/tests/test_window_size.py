import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import (Button, CheckBox, Form, FormBorderStyle, FlatStyle, Label, MenuStrip, ToolStripControlHost,
                                  MouseButtons, ToolStripMenuItem, TextRenderer)
clr.AddReference('System.Drawing')
from System.Drawing import ContentAlignment, Size, Point, Color


class GameWindow(Form):
    def __init__(self):
        self.Size = Size(200, 200)
        self.FormBorderStyle = FormBorderStyle.Sizable
        self._btn = Button()
        self._btn.Parent = self
        self._btn.Location = Point(0, 0)
        self._btn.Size = Size(20, 20)


gw = GameWindow()
gw.ShowDialog()
