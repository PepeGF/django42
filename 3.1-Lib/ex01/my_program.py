from local_lib.path import Path

my_path = Path("wololo")
try:
    my_path.mkdir()
except FileExistsError as e:
    pass
try:
    with open(my_path / "test.txt", "w") as f:
        f.write("PONER LOG Y --FORCE INSTALL EN EL SCRIPT DE INSTALACION")
except Exception as e:
    print(e)
try:
    with open(my_path / "test.txt", "r") as f:
        print(f.read())
except FileNotFoundError as e:
    print(e)
