from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino
import random

class CoffeeMachine:
    def __init__(self):
        self.uses = 0
        self.obsolescence = 10

    class EmptyCup(HotBeverage):
        def __init__(self):
            super().__init__(name="empty cup", price=0.90)

        def description(self):
            return "An empty cup?! Gimme my money back!"
        
    class BrokenMachine(Exception):
        def __init__(self) -> None:
            super().__init__("This coffee machine has to be repaired.")

    def repair(self):
        self.uses = 0
        print("The coffee machine has been repaired.")

    def serve(self, beverage: HotBeverage):
        if self.uses >= self.obsolescence:
            raise self.BrokenMachine()
        # choose randomly among the 4 beverages imported from beverages.py and empty cup
        choice = random.choice([Coffee, Tea, Chocolate, Cappuccino, self.EmptyCup])
        self.uses += 1
        return choice()
    
def test():
    machine = CoffeeMachine()
    for k in range(2):
        for i in range(12):
            try:
                print(machine.serve(HotBeverage()))
            except CoffeeMachine.BrokenMachine as e:
                print(e)
                machine.repair()
            
if __name__ == "__main__":
    test()