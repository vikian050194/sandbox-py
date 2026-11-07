import functools
import time 


def runtime_monitor(input_function):
   @functools.wraps(input_function)
   def runtime_wrapper(*args, **kwargs):
       start_value = time.perf_counter() 
       return_value = input_function(*args, **kwargs)
       end_value = time.perf_counter()
       runtime_value = end_value - start_value 
       print(f"Finished executing {input_function.__name__} in {runtime_value} seconds")
       return return_value
   return runtime_wrapper

def debugging_method(input_function):
   @functools.wraps(input_function)
   def debugging_wrapper(*args, **kwargs):
       arguments = []
       keyword_arguments = []
       for a in args:
          arguments.append(repr(a))    
       for key, value in kwargs.items():
          keyword_arguments.append(f"{key}={value}")
       function_signature = arguments + keyword_arguments
       function_signature = "; ".join(function_signature)      
       print(f"{input_function.__name__} has the following signature: {function_signature}")
       return_value = input_function(*args, **kwargs)
       print(f"{input_function.__name__} has the following return: {return_value}") 
       return return_value
   return debugging_wrapper

def decorator(like):
    print("Inside decorator")
    def inner(func):
        print("Inside inner function")
        print("I like", like) 
        def wrapper():
            func()
        return wrapper
    return inner


@decorator(like="decorators")
def my_func():
    print("Inside actual function")

my_func()


class Box:
    def __init__(self) -> None:
        self.map = {}

    def decorator(self, key: str) -> None:
        def inner(func):
            self.map[key] = func
            return func
        return inner

    def run(self) -> None:
        for k, v in self.map.items():
            print(k)
            v()


b = Box()

@b.decorator(key="Aaa")
def fun1():
    print("inside fun1")

@b.decorator(key="f2")
def fun2():
    print("inside fun2")

b.run()