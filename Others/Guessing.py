import random

def guess_the_number():
    secret_number = random.randint(1, 100)
    attempts = 0
    print("Welcome to the guessing game!")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        guess = int(input("Guess the number: "))
        attempts += 1
        if guess < secret_number:
            print("Too low, try again.")
        elif guess > secret_number:
            print("Too high, try again.")
        else:
            print(f"Congratulations! You guessed the number in {attempts} attempts.")
            break

guess_the_number()