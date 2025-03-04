def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    result = 0
    negative_result = (a < 0) ^ (b < 0)  # XOR to determine if the result should be negative
    a, b = abs(a), abs(b)
    for _ in range(b):
        result += a
    return -result if negative_result else result

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    result = 0
    negative_result = (a < 0) ^ (b < 0)  # XOR to determine if the result should be negative
    a, b = abs(a), abs(b)
    while a >= b:
        a -= b
        result += 1
    return -result if negative_result else result

def calculator():
    print("Welcome to the basic calculator!")
    print("You can perform +, -, *, / operations.")
    print("Enter 'exit' to quit.")
    
    while True:
        user_input = input("\nEnter your operation (e.g., 5 + 3): ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Parse the input
        try:
            parts = user_input.split()
            if len(parts) != 3:
                print("Invalid format. Please use the format: a + b")
                continue
            
            num1 = int(parts[0])
            operator = parts[1]
            num2 = int(parts[2])
            
            if operator == "+":
                print(f"Result: {add(num1, num2)}")
            elif operator == "-":
                print(f"Result: {subtract(num1, num2)}")
            elif operator == "*":
                print(f"Result: {multiply(num1, num2)}")
            elif operator == "/":
                print(f"Result: {divide(num1, num2)}")
            else:
                print("Unsupported operator. Please use +, -, *, or /.")
        except ValueError:
            print("Invalid numbers. Please enter integers.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Lancer la calculatrice
calculator()
