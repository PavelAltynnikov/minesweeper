class Test():
    def __init__(self):
        self._a = 0

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value


t = Test()
print(t.a)
t.a += 1
print(t.a)
t.a += 2
print(t.a)

import pyevent

class MyClass(object):
    OnNewInstance,_NewInstance= pyevent.make_event()
    def __new__(cls):
        res = object.__new__(object)
        MyClass._NewInstance(res)
def NewInst(x): print 'new inst: ', x

MyClass.OnNewInstance += NewInst

a = MyClass()