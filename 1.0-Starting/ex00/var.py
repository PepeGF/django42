def my_var():
    a: int = 42
    b: str = "42"
    c: str = "quarante-deux"
    d: float = 42.0
    e: bool = True
    f: list = [42]
    g: dict = {42 : 42}
    h: tuple = (42,)
    i: set = set()
    print(f"{a} has a type {type(a)}")
    print(f"{b} has a type {type(b)}")
    print(f"{c} has a type {type(c)}")
    print(f"{d} has a type {type(d)}")
    print(f"{e} has a type {type(e)}")
    print(f"{f} has a type {type(f)}")
    print(f"{g} has a type {type(g)}")
    print(f"{h} has a type {type(h)}")
    print(f"{i} has a type {type(i)}")

if __name__ == "__main__":
    my_var()