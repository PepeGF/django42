from local_lib.path import Path

my_path = Path("wololo")
try:
    my_path.mkdir()
except FileExistsError as e:
    print("Directory already exists")
try:
    with open(my_path / "test.txt", "w") as f:
        f.write("Virtual environment and library installed successfully!")
except Exception as e:
    print(e)
try:
    with open(my_path / "test.txt", "r") as f:
        print(f.read())
except FileNotFoundError as e:
    print(e)
