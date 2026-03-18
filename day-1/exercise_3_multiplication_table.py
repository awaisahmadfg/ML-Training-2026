def get_number_1_to_12():
    """Ask the user for an integer 1–12 and return it."""
    while True:
        user_input = input("Enter a number between 1 and 12: ")

        try:
            n = int(user_input)
        except ValueError:
            print("That is not a number. Please try again.")
            continue

        if 1 <= n <= 12:
            return n
        else:
            print("Number must be between 1 and 12. Please try again.")


def print_table(n):
    """Print a single multiplication table for n (1–12)."""
    print(f"\nMultiplication table for {n}:\n")
    for i in range(1, 13):
        print(f"{n:>2} x {i:>2} = {n * i:>4}")


def print_all_tables():
    """Print multiplication tables for 1–12."""
    print("\nFull tables from 1 to 12:\n")
    for n in range(1, 13):
        print_table(n)
        print()  # blank line between tables


def main():
    n = get_number_1_to_12()
    print_table(n)
    print_all_tables()


if __name__ == "__main__":
    main()