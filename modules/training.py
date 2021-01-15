import time
from modules.inbox import *
from modules.login_notifications import *
from modules.login import *
from modules.friend_search import *


def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


def print_training_options():
    message = """
    Training
    ------------------
    1.) Training and Education
    2.) IT Help Desk
    3.) Business Analysis and Strategy
    4.) Security
    5.) Go back
"""
    print(message)


def print_business():
    message = """
        Trending courses
        ------------------
        1.) How to use In College learning
        2.) Train the trainer
        3.) Gamification of learning
        
Not seeing what you’re looking for? Sign in to see all 7,609 results by selection 4  
"""
    print(message)


def print_train_edu():
    message = """
        Training and Education
        ------------------
        1.) Definition
        2.) Differences
        3.) Career
        4.) Comparison
        5.) Go back
    """
    print(message)


def train_edu(option):
    if option == 1:
        print("Under construction!")
    if option == 2:
        print("Under construction!")
    if option == 3:
        print("Under construction!")
    if option == 4:
        print("Under construction!")
    if option == 5:
        return False
    time.sleep(2)
    return True


def training_selection(option):
    if option == 1:  # train/edu
        while True:
            print_train_edu()
            option = get_user_option(1, 5)
            while option < 1 or option > 5:
                print("Invalid input. Try again")
                option = get_user_option(1, 5)
            process = train_edu(option)
            if not process:
                return True
    if option == 2:
        print("Coming soon!")
    if option == 3:  # business
        while True:
            print_business()
            option = get_user_option(1, 4)
            while option < 1 or option > 4:
                print("Invalid input. Try again")
                option = get_user_option(1, 4)
            # login if any selection is chosen
            if LOGGED_IN_USER.get("username", None):
                break
            print("""
------------------
      Login      |
------------------""")
            username = input("Please enter a username: ")
            password = input("Please enter a password: ")
            logged_in = login(username, password)
            if logged_in:
                # Show pending friend requests and allow user to accept or decline them
                profile_notification()
                has_requests = show_requests()
                answer = has_inbox()
                return 2  # if login successfully then return 2
            else:
                return 1
    if option == 4:
        print("Coming soon!")
    if option == 5:
        return 0  # 0 to go back to previous menu
    time.sleep(2)
    return 1
