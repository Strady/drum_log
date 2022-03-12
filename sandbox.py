from objdict import ObjDict


class A:
    data = ObjDict()


class B(A):

    def add(self):
        self.data.something = ['something']


class C(A):

    def add(self):
        self.data.anything = ['anything']


b = B()
c = C()

b.add()
c.add()
print(A.data)
print(b.data)
print(c.data)