"""Simple Calculator.

This module is a training task of week 6.
Simple calculator to get in touch with try-except and raises.
"""

class Calculator:
    def add(self, a, b):
        return a + b
    
    def substract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Teilen durch 0 ist nicht möglich")
        return a / b
    
    def choose_operator(self):

        operator = input("Wähle den Rechenoperator aus (+, -, *, /): ")
        if operator in ('+', '-', '*', '/'):
            return operator
        else:
            raise ValueError("Ungültiger Rechenoperator!")

    def perform_operator(self, a, b, operator):
            
            if operator == '+':
                return self.add(a, b)

            elif operator == '-':
                return self.substract(a, b)
            
            elif operator == '*':
                return self.multiply(a, b)

            else:
                return self.divide(a, b)

    def perform_calculator(self):
        try:
            num1 = float(input("Erste Ziffer: "))
            num2 = float(input("Zweite Ziffer: "))
            operator = self.choose_operator()
            result = self.perform_operator(num1, num2, operator)
            print(f"Rechnung: {num1} {operator} {num2} = {result}")
        except ValueError as e:
            print(e)
    
    
calc = Calculator()
calc.perform_calculator()