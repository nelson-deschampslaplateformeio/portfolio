import os
import json

# Check or initialize the JSON file
if not os.path.exists("history.json"):
    with open("history.json", "w") as file: 
        json.dump({"calculations": []}, file)  # Initialize with an empty structure

# This function adds two numbers
def add(x, y):
    return x + y

# This function subtracts two numbers
def subtract(x, y):
    return x - y

# This function multiplies two numbers
def multiply(x, y):
    return x * y

# This function divides two numbers
def divide(x, y):
    if  y == 0:
        return "Error: Division by zero."
    return x / y

# Initialize history
history = []

# Classic calculator function
def classic_calculator():
    print("\nClassic Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    while True:
        choice = input("\nEnter choice (1/2/3/4): ")

        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue

            if choice == '1':
                result = add(num1, num2)
                print(num1, "+", num2, "=", result)
                write_json(num1, choice, num2, result)
            elif choice == '2':
                result = subtract(num1, num2)
                print(num1, "-", num2, "=", result)
                write_json(num1, choice, num2, result)
            elif choice == '3':
                result = multiply(num1, num2)
                print(num1, "*", num2, "=", result)
                write_json(num1, choice, num2, result)
            elif choice == '4':
                result = divide(num1, num2)
                print(num1, "/", num2, "=", result)
                write_json(num1, choice, num2, result)
            
        while True:
            next_calculation = input("\nDo you want another calculation? (yes/no): ").strip().lower()
            if next_calculation == "no":
                return False  
            elif next_calculation == "yes":
                break  
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
            

# Custom calculator function
def custom_calculator():
    def calculate(expression):
        expression = expression.replace(" ", "")
        valid_chars = "0123456789.+-*/"
        if not all(char in valid_chars for char in expression):
            return "Invalid characters in expression."

        numbers = []
        operators = []
        i = 0
        while i < len(expression):
            num = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                num += expression[i]
                i += 1
            if num:
                numbers.append(float(num))
            if i < len(expression) and expression[i] in "+-*/":
                operators.append(expression[i])
                i += 1

        if len(numbers) - 1 != len(operators):
            return "Invalid expression format."

        while "*" in operators or "/" in operators:
            for i, op in enumerate(operators):
                if op in "*/":
                    if op == "*":
                        result = numbers[i] * numbers[i + 1]
                    elif op == "/":
                        if numbers[i + 1] == 0:
                            return "Error: Division by zero."
                        result = numbers[i] / numbers[i + 1]
                    numbers[i] = result
                    del numbers[i + 1]
                    del operators[i]
                    break

        while "+" in operators or "-" in operators:
            for i, op in enumerate(operators):
                if op in "+-":
                    if op == "+":
                        result = numbers[i] + numbers[i + 1]
                    elif op == "-":
                        result = numbers[i] - numbers[i + 1]
                    numbers[i] = result
                    del numbers[i + 1]
                    del operators[i]
                    break

            
        return numbers[0]
    

    print("\nCustom Calculator")
    print("Enter expressions like: a.1 + b - c.5 * d / e")

    while True:
# Ask the user to enter an expression and calculate the result
        expression = input("\nEnter your expression: ").strip()
        try:
            result = calculate(expression)
            print(f"Result; {result}")
            write_json(expression, None, None, result) 
        except Exception as e:
         print(f"Error: {e}. Please enter a valid expression.")
    
# Loop to validate the response to the question
        while True:
            next_calculation = input("\nDo you want another calculation? (yes/no): ").strip().lower()
            if next_calculation == "no":
                return False  
            elif next_calculation == "yes":
                break  
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


        

def write_json(num1, choice, num2, result):
    with open("history.json", "r+") as file:
        data = json.load(file)  # Charge les données existantes
        if num1 is None and choice is None and num2 is None:
            # Cas d'une expression brute
            data["calculations"].append({
                "expression": result,  # Enregistre l'expression brute avec son résultat
                "result": result
            })
        else:
            # Cas classique
            data["calculations"].append({
                "choice": choice,
                "num1": num1,
                "num2": num2,
                "result": result
            })
        file.seek(0)  # Retourne au début du fichier
        json.dump(data, file, indent=4)  # Écrit les nouvelles données


def read_history():
    with open("history.json", "r") as file:
        data = json.load(file)  # Charge les données de l'historique
        if data["calculations"]:
            print("\nCalculation History:")
            for calc in data["calculations"]:
                if "expression" in calc:
                    # Affiche une expression brute
                    print(f"Expression: {calc['expression']} = {calc['result']}")
                else:
                    # Affiche un calcul classique
                    print(f"{calc['num1']} {calc['choice']} {calc['num2']} = {calc['result']}")
        else:
            print("No calculations found in history.")
      

# Main menu
def main():
    while True:
        print("\nMain Menu")
        print("1. Classic Calculator")
        print("2. Custom Calculator")
        print("3. Show History")
        print("4. Exit")

        choice = input("\nChoose an option (1/2/3/4): ").strip()

        if choice == "1":
            classic_calculator()
        elif choice == "2":
            custom_calculator()
        elif choice == "3":
            read_history()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
main()