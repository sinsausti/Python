# Description:
# A secure password generator that creates random passwords based on user-specified criteria, such as length, and whether to include uppercase letters, digits, and symbols.

# Usage:
# python PasswordGenerator.py

import random
import string

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def password_generator():
    print("Welcome to the Password Generator!")

    length = int(input("Enter the desired length of the password: "))
    use_upper = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
    use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'

    password = generate_password(length, use_upper, use_digits, use_symbols)
    print(f"Generated password: {password}")

password_generator()