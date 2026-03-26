# import library installed on ../local_lib
import sys
sys.path.append('../local_lib')
import path
import inspect

print(inspect.getmodule(path).__file__)

