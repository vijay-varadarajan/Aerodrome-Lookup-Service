import csv
import pwinput
import string
from voice import say
from signup import decrypt_password, sign_up


ALL_KEYS = string.ascii_letters + string.digits + string.punctuation


def log_in():
    username, password = get_login_data()
    if check_login_data(username, password):
        say("Logged in")
        print("Logged in")
        say(f"Welcome, {username}")
        print(f"Welcome, {username}")
        return True


def get_login_data():
    while True:
        say("Enter username")
        username = input("Username: ")
        if not check_username(username):
            print("Username unavailable")
            say("Username unavailable, do you want to sign up?")
            choice = input("Do you want to sign up [y/n]? ").strip().lower()
            if "y" in choice:
                sign_up()
                break
            else:
                print("Try again")
                say("Try again")
            continue
        else:
            break

    wrong_pass = 0
    say("Enter password to login: ")
    while True:
        password = pwinput.pwinput(prompt="Password: ", mask="*")
        if not check_password(username, password):
            print("Wrong password, try again!")
            say("Wrong password, try again")
            wrong_pass += 1

            if wrong_pass > 3:
                say("Do you want to sign up?")
                choice = input("Do you want to sign up [y/n]? ").strip().lower()
                if "y" in choice:
                    sign_up()
                    break
            continue
        else:
            break

    return username, password


def check_login_data(username, password):
    if check_username(username) and check_password(username, password):
        return True


def check_username(username):
    with open("users.csv", "r") as users:
        reader = csv.DictReader(users)
        for row in reader:
            if row["username"] == username:
                return True
    return False


def check_password(username, password):
    with open("users.csv", "r") as users:
        reader = csv.DictReader(users)
        for row in reader:
            if (
                row["username"] == username
                and decrypt_password(username, row["password"]) == password
            ):
                return True
    return False
