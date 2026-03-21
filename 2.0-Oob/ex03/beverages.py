class HotBeverage:
    def __init__(self, name: str="hot beverage", price: float=0.30):
        self.price = price
        self.name = name

    def description(self):
        return "Just some hot water in a cup."

    def __str__(self):
        return (f"name : {self.name}\n" +
                f"price : {self.price:.2f}\n" +
                f"description : {self.description()}\n")
    
class Coffee(HotBeverage):
    def __init__(self):
        super().__init__(name="coffee", price=0.40)

    def description(self):
        return "A coffee, to stay awake."

class Tea(HotBeverage):
    def __init__(self):
        super().__init__(name="tea", price=0.30)

    def description(self):
        return "Just some hot water in a cup."
    
class Chocolate(HotBeverage):
    def __init__(self):
        super().__init__(name="chocolate", price=0.50)

    def description(self):
        return "Chocolate, sweet chocolate..."
    
class Cappuccino(HotBeverage):
    def __init__(self):
        super().__init__(name="cappuccino", price=0.45)

    def description(self):
        return "Un po' di Italia nella sua tazza!"
    
def test():
    print(HotBeverage())
    print(Coffee())
    print(Tea())
    print(Chocolate())
    print(Cappuccino())

if __name__ == "__main__":
    test()