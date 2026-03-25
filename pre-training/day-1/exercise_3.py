while True:
    user_input = input("Enter a number (1-12): ").strip()
    if user_input.isdigit():
        number = int(user_input)
        if 1 <= number <= 12:
            break
    print("Invalid input. Please try again.")

def print_table(n: int) -> None:
    width = len(str(n * 12))
    for i in range(1, 13):
        result = n * i
        print(f"{n:>2} x {i:>2} = {result:>{width}}")


print_table(number)
print()

for n in range(1, 13):
    print_table(n)
    if n != 12:
        print()

