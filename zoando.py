print("'Hello, World!'")
print("im coming for you!")
# this is a test for the new code editor
#----------------------------------------------------------------------------------------------
name = "wadley"
age = 15
name = input("what is your name? ")
age = input("what is your age? ")
print("Hello," + name + "! You are " + age + " years old.")

#math
print("math time!")
input("are u ready"  + name + "?")
a = "yes"
if a == "yes":
    print("ok lets do some math!")
else:
    print("ok maybe next time")

print("which math problem do you want to do?")
print("1. addition")
print("2. subtraction")
print("3. multiplication")
math_problem = input("choose a number: ")
if math_problem == "1":
    num1 = int(input("enter a number: "))
    num2 = int(input("enter another number: "))
    print(num1 + num2)
elif math_problem == "2":
    num1 = int(input("enter a number: "))
    num2 = int(input("enter another number: "))
    print(num1 - num2)
elif math_problem == "3":
    num1 = int(input("enter a number: "))
    num2 = int(input("enter another number: "))
    print(num1 * num2)

# if the user wants to do another math problem
while True:
    continue_math = input("do you want to do another math problem? (yes/no): ")
    if continue_math == "yes":
        print("which math problem do you want to do?")
        print("1. addition")
        print("2. subtraction")
        print("3. multiplication")
        math_problem = input("choose a number: ")
        if math_problem == "1":
            num1 = int(input("enter a number: "))
            num2 = int(input("enter another number: "))
            print(num1 + num2)
        elif math_problem == "2":
            num1 = int(input("enter a number: "))
            num2 = int(input("enter another number: "))
            print(num1 - num2)
        elif math_problem == "3":
            num1 = int(input("enter a number: "))
            num2 = int(input("enter another number: "))
            print(num1 * num2)
    else:
        print("want to play a new game?")
        break
new_game = input("do you want to play a new game? (yes/no): ")
if new_game == "yes":
    print("ok lets play a new game!")
    print("i got a new game for you!")
new_game = input("are you curious? (yes/no): ")
if new_game == "yes":
    print("its guess my number!")
    #computer picks a random number between 1 and 10
    import random
    number = random.randint(1, 10)
    print("i have a number between 1 and 10. can you guess it?")
    #user has 3 tries to guess the number
    for i in range(3):
        guess = int(input("enter your guess: "))
        if guess == number:
            print("you guessed it! the number was " + str(number))
            break
        else:
            print("wrong guess. try again.")
    else:
        print("sorry, you ran out of tries. the number was " + str(number))
        while True:
            play_again = input("do you want to play again? (yes/no): ")
            if play_again == "yes":
                number = random.randint(1, 10)
                print("i have a new number between 1 and 10. can you guess it?")
                for i in range(3):
                    guess = int(input("enter your guess: "))
                    if guess == number:
                        print("you guessed it! the number was " + str(number))
                        break
                    else:
                        print("wrong guess. try again.")
                else:
                    print("sorry, you ran out of tries. the number was " + str(number))
            else:
                print("ok maybe next time")
                break
else:
    print("ok maybe next time")
