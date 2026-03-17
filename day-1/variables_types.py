def main() -> None:
    name: str = "Awais Ahmad"
    age: int = 26
    drinks_coffee: bool = True
    salary: float = 85000.0 

    # Formatted sentence using all four variables
    coffee_text = "do" if drinks_coffee else "don't"
    print(f"My name is {name}, I am {age} years old, I {coffee_text} drink coffee, and my salary is Rs. {salary:,.2f} per month.")

    # Years until retirement at 60
    retirement_age: int = 60
    years_to_retire: int = retirement_age - age
    if years_to_retire > 0:
        print(f"Years until retirement (at {retirement_age}): {years_to_retire}")
    elif years_to_retire == 0:
        print(f"You are retiring this year (age {retirement_age}).")
    else:
        print(f"You already passed retirement age by {-years_to_retire} years.")

    cups_per_day: int = 3
    price_per_cup: int = 150
    days_per_week: int = 7

    weekly_coffee_budget: int = cups_per_day * price_per_cup * days_per_week
    weekly_coffee_budget = weekly_coffee_budget if drinks_coffee else 0

    print(f"Weekly coffee budget: Rs. {weekly_coffee_budget:,}")


if __name__ == "__main__":
    main()