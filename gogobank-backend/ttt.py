import time
def custom_decorator(func):
    def my_function(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")

    
    return my_function

try:
    #raise ValueError("This is a sample error")  # Simulating an error
    3/0
except ValueError as e:
    print("An error occurred:", str(e))
except Exception as e:
    print("A general exception occurred:", str(e))

# def sum(a,b):
#     time.sleep(2)
#     raise Exception
#     return a + b

# @custom_decorator
# def rum(a,b):
#     time.sleep(2)
#     return a / b

# custom_decorator(sum)(2,3)

# rum(2,1)

# def q(*args, **kargs):
#     print(args)
#     print(kargs)

# def sum_all(*args):
#     total = 0
#     for num in args:
#         total += num
#     return total

# q(1,2,3,4,5,6,name="bidis",age=22)
# print(sum_all(1,2,3,4,5,6,7,8,9,20))

class A:
    b = 3
    c = 5

print(A.b)
print(getattr(A,'b'))