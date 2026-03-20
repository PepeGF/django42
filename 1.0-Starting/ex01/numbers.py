def print_numbers():
    with open("../attached/ex01/numbers.txt", "r") as file:
        numbers = file.read().split(",")
    [print(int(number)) for number in numbers]

if __name__ == "__main__":
    print_numbers()
