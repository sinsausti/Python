# Description:
# A command-line scientific calculator that supports a variety of mathematical operations, including addition, subtraction, 
# multiplication, division, power, sine, cosine, tangent, logarithm, and exponential functions. 

# Usage:
# python Calculator.py

import math

def scientific_calculator():
    print("Welcome to the Scientific Calculator!")
    print("Available operations: add, subtract, multiply, divide, sin, cos, tan, log, exp, pow, quit")

    while True:
        operation = input("Enter operation: ").strip().lower()
        
        if operation == 'quit':
            break

        if operation in ['add', 'subtract', 'multiply', 'divide', 'pow']:
            x = float(input("Enter first number: "))
            y = float(input("Enter second number: "))

        if operation == 'add':
            result = x + y
        elif operation == 'subtract':
            result = x - y
        elif operation == 'multiply':
            result = x * y
        elif operation == 'divide':
            if y != 0:
                result = x / y
            else:
                result = "Error: Division by zero"
        elif operation == 'pow':
            result = math.pow(x, y)
        elif operation == 'sin':
            x = float(input("Enter number: "))
            result = math.sin(math.radians(x))
        elif operation == 'cos':
            x = float(input("Enter number: "))
            result = math.cos(math.radians(x))
        elif operation == 'tan':
            x = float(input("Enter number: "))
            result = math.tan(math.radians(x))
        elif operation == 'log':
            x = float(input("Enter number: "))
            if x > 0:
                result = math.log(x)
            else:
                result = "Error: Logarithm of non-positive number"
        elif operation == 'exp':
            x = float(input("Enter number: "))
            result = math.exp(x)
        else:
            result = "Error: Unsupported operation"

        print(f"Result: {result}")

scientific_calculator()