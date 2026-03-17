name = "Saqib"
age = 25
drinks_coffee = True
salary = 100000.0

print(f"My name is {name}. I am {age} years old. Drinks coffee: {drinks_coffee}. Salary: Rs. {salary}.")

retirement_age = 60
years_until_retirement = retirement_age - age
print(f"Years until retirement: {years_until_retirement}")

cups_per_day = 3
cup_price = 150
days_per_week = 7
weekly_coffee_budget = cups_per_day * cup_price * days_per_week if drinks_coffee else 0
print(f"Weekly coffee budget: Rs. {weekly_coffee_budget}")

