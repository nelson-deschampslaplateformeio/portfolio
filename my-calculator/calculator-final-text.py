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
    if y == 0:
        return "Error: Division by zero."
    return x / y

# Function to save calculation history
def write_history(entry):
    with open('history.txt', 'a') as history_file:
        history_file.write(entry + '\n')

# Function to read history
def read_history():
    try:
        with open('history.txt', 'r') as history_file:
            print("Calculation History:")
            print(history_file.read())
    except FileNotFoundError:
        print("No history available.")

# Function to delete history
def delete_history():
    with open('history.txt', 'w') as history_file:
        history_file.truncate(0)
        print("History deleted.")

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
                operation = "+"
            elif choice == '2':
                result = subtract(num1, num2)
                operation = "-"
            elif choice == '3':
                result = multiply(num1, num2)
                operation = "*"
            elif choice == '4':
                result = divide(num1, num2)
                operation = "/"

            print(f"{num1} {operation} {num2} = {result}")
            write_history(f"{num1} {operation} {num2} = {result}")

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
        try:
            result = eval(expression)
            return result
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception:
            return "Invalid expression."

    print("\nCustom Calculator")
    print("Enter expressions like: 2 + 3 * 5 / 7 - 1")

    while True:
        expression = input("\nEnter your expression: ").strip()
        result = calculate(expression)

        if isinstance(result, str):
            print(result)
        else:
            print(f"Result: {result}")
            write_history(f"{expression} = {result}")

        while True:
            next_calculation = input("\nDo you want another calculation? (yes/no): ").strip().lower()
            if next_calculation == "no":
                return False  
            elif next_calculation == "yes":
                break  
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

# Main menu
def main():
    while True:
        print("\nMain Menu")
        print("1. Classic Calculator")
        print("2. Custom Calculator")
        print("3. Show History")
        print("4. Delete History")
        print("5. Exit")

        choice = input("\nChoose an option (1/2/3/4/5): ").strip()

        if choice == "1":
            classic_calculator()
        elif choice == "2":
            custom_calculator()
        elif choice == "3":
            read_history()
        elif choice == "4":
            delete_history()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
main()
