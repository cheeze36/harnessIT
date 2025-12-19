def get_income():
    income = float(input("Enter your monthly income: $"))
    return income

def get_fixed_expenses():
    fixed = float(input("Enter your total fixed expenses : $"))
    return fixed

def get_variable_expenses():
    variable_total = 0.0
    print("Enter your variable expenses. Type 'done' when finished.")
    while True:
        reply = input("Expense name (or 'done'): ")
        if reply.lower() == 'done':
            break
        try:
            amount = float(input(f"Amount for {reply}: $"))
            variable_total += amount
        except ValueError:
            print("Invalid amount. Please enter a number.")
    return variable_total

def calculate_budget(income, fixed, variable):
    remaining = income - (fixed + variable)
    return remaining

def debug_budget(income, fixed, variable, remaining):
    print("\n--- Debugging Info ---")
    print(f"Income: ${income}")
    print(f"Fixed Expenses: ${fixed}")
    print(f"Variable Expenses: ${variable}")
    print(f"Remaining Budget (calculated): ${remaining}")
    expected = income - (fixed + variable)
    print(f"Expected Budget: ${expected}")
    if remaining != expected:
        print(" Logical error detected in budget calculation.")
    else:
        print("Budget calculation is correct.")

def main():
    print("=== Monthly Budget Calculator ===")
    income = get_income()
    fixed = get_fixed_expenses()
    variable = get_variable_expenses()
    remaining = calculate_budget(income, fixed, variable)
    if remaining < 0:
        print(f"\nYour budget is negative: -${abs(remaining):.2f}. Consider reducing expenses.")
    elif remaining < 100:
        print(f"\nYour remaining budget is low: ${remaining:.2f}. Spend cautiously.")
    else:
        print(f"\nYou have ${remaining:.2f} left this month. Great job!")
    debug_budget(income, fixed, variable, remaining)
main()