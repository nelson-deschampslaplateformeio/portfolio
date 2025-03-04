



             



print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")

while True:
    # take input from the user
    choice = input("Enter choice(1/2/3/4): ")

    # check if choice is one of the four options
    if choice in ('1', '2', '3', '4'):
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # This function adds two numbers
        def add(a, b):
            return a + b
        
        # This function subtracts two numbers
        def subtract(a, b):
            return a - b
        
        # This function multiplies two numbers
        def multiply(a, b):
            return a * b
         

        # This function divides two numbers
        def divide(a, b):
            if b or a == 0:
                return "Error: Division by zero."
            return a / b
              
        

        if choice == '1':
            print(a, "+", b, "=", add(a, b))


        elif choice == '2':
            print(a, "-", b, "=", subtract(a, b))

        elif choice == '3':
            print(a, "*", b, "=", multiply(a, b))

        elif choice == '4':
            print(a, "/", b, "=", divide(a, b))
        # check if user wants another calculation
        # break the while loop if answer is no
        next_calculation = input("Let's do next calculation? (yes/no): ")
        if next_calculation == "no":
          break
        else:
            print("Invalid Input")