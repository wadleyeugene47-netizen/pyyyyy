import random


def print_dice(die1, die2):
    """Print the two dice results in a readable format."""
    print(f"You rolled: {die1} and {die2}")


while True:
    user_choice = input("Roll the dice? (y/n): ").strip().lower()

    if user_choice == "y":
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        print_dice(die1, die2)
    elif user_choice == "n":
        print("Thank you for playing!")
        break
    else:
        print("Invalid choice. Please enter y or n.")