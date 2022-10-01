class Foo:
    def __init__(self, apple : int):
        self.banana = apple

classes = [Foo]
test = classes[0](1)
print(test.banana)