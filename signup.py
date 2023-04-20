import csv
import pwinput
import string
from voice import say


ALL_KEYS = string.ascii_letters + string.digits + string.punctuation


def sign_up():
    username, password = False, False
    while not username or not password:
        username, password = get_signup_data()
    upload_signup_data(username, password)

    say(f"Signed in as {username}")
    print(f"Signed in as {username}")
    return True


def get_signup_data():
    say("Enter username")
    while True:
        username = input("Username: ")
        if not username:
            print("Please enter a username.")
            say("Please enter a username.")
            continue
        elif not check_username(username):
            print("Username taken. Enter different username.")
            say("Username taken. Enter different username.")
            continue
        else:
            break

    say("Enter password")
    while True:
        password = pwinput.pwinput(prompt="Password: ", mask="*")
        if not check_password(password):
            print(
                "Password must contain atleast 2 letters, 2 numbers, 1 symbol and no white space. Try again."
            )
            say(
                "Password must contain atleast 2 letters, 2 numbers, 1 symbol and no white space. Try again."
            )
            continue
        else:
            break

    attempts = 0
    say("Enter password again for confirmation.")
    while True:
        confirm_password = pwinput.pwinput(prompt="Confirm password: ", mask="*")
        if not password == confirm_password:
            print("Confirm password must be same as password. Try again.")
            say("Confirm password must be same as password. Try again.")
            attempts += 1
            if attempts > 3:
                print("Maximum attempts reached. Please start again.")
                say("Maximum attempts reached. Please start again.")
                return False, False
            continue
        else:
            break

    return username, password


def upload_signup_data(username, password):
    with open("users.csv", "a") as users:
        fields = [username, password]
        writer = csv.DictWriter(users, fieldnames=fields)
        writer.writerow(
            {username: username, password: encrypt_password(username, password)}
        )


def check_username(username):
    with open("users.csv", "r") as users:
        reader = csv.DictReader(users)
        for row in reader:
            if row["username"] == username:
                return False
    return True


def check_password(pwd):
    char_count, num_count, punc_count = 0, 0, 0
    for char in pwd:
        if char in string.ascii_letters:
            char_count += 1
        elif char in string.digits:
            num_count += 1
        elif char in string.punctuation:
            punc_count += 1
        else:
            pass

    if char_count >= 2 and num_count >= 2 and punc_count >= 1:
        return True
    return False


def encrypt_password(username, pwd):
    new_pwd = ""
    key = len(username)
    for letter in pwd:
        new_position = (ALL_KEYS.find(letter) + key) % len(ALL_KEYS)
        new_pwd += ALL_KEYS[new_position]
    return new_pwd


def decrypt_password(username, pwd):
    old_pwd = ""
    key = len(username)
    for letter in pwd:
        new_position = (ALL_KEYS.find(letter) - key) % len(ALL_KEYS)
        old_pwd += ALL_KEYS[new_position]
    return old_pwd
