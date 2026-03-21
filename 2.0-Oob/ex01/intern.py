class Intern():
    def __init__(self, name: str = "My name? I'm nobody, an intern, I have no name."):
        self.name = name

    def work(self):
        raise Exception("I'm just an intern, I can't do that...")
    
    def make_coffee(self):
        return self.Coffee()

    def __str__(self):
        return self.name
    
    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."
        

def test():
    intern = Intern()
    print(intern)
    try:
        intern.work()
    except Exception as e:
        print(e)
    print(intern.make_coffee())

    mark = Intern("Mark")
    print(mark)
    print(mark.make_coffee())
    try:
        mark.work()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test()