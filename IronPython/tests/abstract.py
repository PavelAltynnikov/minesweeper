from abc import abstractmethod


class TestABC():
    @abstractmethod
    def test(self):
        pass


class Test(TestABC):
    def some_method(self):
        print(123)


t = Test()
t.some_method()
