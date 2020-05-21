# -*- coding: utf-8 -*-
class Test():
    def __init__(self):
        self._a = 0
        self.__x = 0

    def getx(self):
        return self.__x

    def setx(self, value):
        print("Нельзя сделать _a отрицательным")
        self.__x = value
        return None

    def delx(self):
        del self.__x

    x = property(fget=getx, fset=setx, fdel=delx, doc="I'm the 'x' property.")


t = Test()
# print(t.a)
# t.a += 1
# print(t.a)
# t.a += 2
# print(t.a)
# t.a -= 2
# print(t.a)
# t.a -= 1
# print(t.a)
# t.a -= 3
# print(t.a)
print(t.x)
t.x = 10
t.x(20)
