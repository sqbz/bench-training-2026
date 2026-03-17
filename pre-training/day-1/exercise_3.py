while True:
    user_input = input("Enter a number (1-12): ").strip()
    if user_input.isdigit():
        number = int(user_input)
        if 1 <= number <= 12:
            break
    print("Invalid input. Please try again.")

width = len(str(number * 12))
for i in range(1, 13):
    result = number * i
    print(f"{number:>2} x {i:>2} = {result:>{width}}")

