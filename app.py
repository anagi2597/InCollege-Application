# This file contains all the functions and code to run our application
# Refer to test_app file for pytest methods

import json
import time
from modules.find import *
from modules.login import *
from modules.register import *
from modules.skills import *
from modules.welcome import *
from modules.jobs import *
from modules.useful_links import *
from modules.importantLinks import *
from modules.profile import *
from modules.profile_view import *
from modules.friend_search import *
from modules.jobs2 import *
from modules.del_show_jobs import *
from modules.messaging import *
from modules.inbox import *
from modules.login_notifications import *
from modules.noti_group import *
from modules.training import *
from modules.learning import *
from API.savedJobs import *
from API.appliedJobs import *
from API.writeTraining import *
from API.userTier import *
from API.writeProfile import *
from API.api import *
from modules.find import *


def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


if __name__ == "__main__":
    with open("database.json", "r") as db:
        data = json.load(db)
        db.close()

    with open("database.json", "w+") as db:
        for user in data["users"]:
            if not user.get("posted_title", None):
                user["posted_title"] = {}

        json.dump(data, db)
        db.close()
    new_training=[]
    while True:
        print_welcome()
        option = get_user_option(1, 7)
        while option < 1 or option > 7:
            print("Invalid input. Try again")
            option = get_user_option(1, 7)
        if option == 1:  # Login
            if LOGGED_IN_USER.get("username", None):
                break
            username = input("Please enter a username: ")
            password = input("Please enter a password: ")
            logged_in = login(username, password)
            if logged_in:
                # Show pending friend requests and allow user to accept or decline them
                profile_notification()
                has_requests = show_requests()
                answer = has_inbox()
                break
            else:
                continue
        elif option == 2:  # Create new account
            registered = register()
            if not registered:
                exit()
            else:
                continue
        elif option == 3:
            print_useful_links()
            continue
        elif option == 4:
            while True:
                important_links()
                option = get_user_option(1, 9)
                process = process_important_link(option)
                if not process:
                    break
        elif option == 5:  # Watch Video
            print("Video is now playing for the next 5 seconds")
            time.sleep(5)
            continue
        elif option == 6:  # training
            res = 1  # 1 by default means keep looping until 0 or 2
            while True:
                print_training_options()
                option = get_user_option(1, 5)
                while option < 1 or option > 5:
                    print("Invalid input. Try again")
                    option = get_user_option(1, 5)
                res = training_selection(option)
                if res == 0:  # 0 means not logged in but go back
                    break
                elif res == 2:  # 2 means logged in
                    break
            if res == 2:
                break
        elif option == 7:
            api_account()
            api_writeJobs()
            api_newJobs()
            writeProfile()
            writeTiers()
            writeTraining()
            writeSavedJobs()
            writeAppliedJobs()
            new_training = api_training()
            LOGGED_IN_USER = {}

    while True:
        check_new_reg()
        check_delete_job()
        time.sleep(5)
        print_welcome2()
        option = get_user_option(1, 14)
        while option < 1 or option > 14:
            print("Invalid input. Try again")
            option = get_user_option(1, 14)

        if option == 1:  # Post Job
            print("Posting Job")
            title = input(
                "Please enter the title of the job you are posting: ")
            description = input(
                "Please enter the description of the job you are posting: ")
            employer = input(
                "Please enter the name of the employer for this job: ")
            location = input("Please enter the location of this job: ")
            salary = input("Please enter the salary of this job: ")

            job_posted = post_job(title, description,
                                  employer, location, salary, 'database.json')
            continue
        elif option == 2:  # Search for a job
            while True:
                applied_for_jobs()
                time.sleep(2)
                print("")
                jobs = get_all_jobs()
                new_jobs_notification(jobs)
                print("")
                print_all_jobs(jobs)
                option = job_options()
                while not validate_job_option(option):
                    option = job_options()

                if option == 'x':
                    print("Going back to main menu")
                    break
                user_choice = get_user_option(1, len(jobs))
                while user_choice < 1 or user_choice > len(jobs):
                    print("Invalid input. Try again")
                    user_choice = get_user_option(1, len(jobs))

                processed_option = process_option(
                    option, jobs[user_choice - 1])
                print("")
                if not processed_option[0]:
                    if processed_option[1] == 'x':
                        print("Going back to main menu")
                    elif processed_option[1] != 'a':
                        print("An error occurred. Going back to main menu")
                        break
                time.sleep(2)
            time.sleep(2)
            continue
        elif option == 3:  # Manage jobs
            check_last_applied()
            while True:
                applied_for_jobs()
                time.sleep(2)
                jobs = get_all_jobs()
                new_jobs_notification(jobs)
                print_manage_jobs()
                user_choice = get_user_option(1, 5)
                while user_choice < 1 or user_choice > 5:
                    print("Invalid input. Try again")
                    user_choice = get_user_option(1, 5)
                if user_choice == 1:  # Delete a job
                    deleted = delete_job()
                elif user_choice == 2:  # View saved jobs
                    edit_saved = edit_saved_jobs()
                elif user_choice == 3:  # View applied jobs
                    printApplied = print_applied_jobs()
                elif user_choice == 4:  # View jobs not applied for
                    notApplied = print_not_applied()
                else:
                    break

        elif option == 4:  # Find user
            first_name = input(
                "Enter the first name of the user you want to find: ")
            last_name = input(
                "Enter the last name of the user you want to find: ")
            userFound = find_user(first_name, last_name, 'database.json')
            if userFound:
                print('1.) Login and contact your friends')
                print('2.) Sign up and join your friends')
                print('Enter 0 to go back to main menu')
                option = int(input("Enter your option: "))
                if option == 0:
                    continue
                elif option == 1:
                    username = input("Please enter a username: ")
                    password = input("Please enter a password: ")
                    logged_in = login(username, password)
                    if logged_in:
                        continue
                elif option == 2:
                    registered = register()
                    if not registered:
                        exit()
                    else:
                        continue
        elif option == 5:  # Learn skill
            option = list_of_skills()
            while option[0] < 1 or option[0] > 6:
                print("Invalid input. Try again")
                option = list_of_skills()
            if option[0] <= 5:
                print("Under Construction")
                time.sleep(1)
            else:
                time.sleep(1)
                continue
        elif option == 6:
            print_useful_links()
        elif option == 7:
            while True:
                important_links()
                option = get_user_option(1, 9)
                process = process_important_link(option)
                if not process:
                    break
        # The following is for Epic 4.
        elif option == 8:
            while True:
                profile_options = """
                --Profiles--
                1.) View profile
                2.) Create profile
                3.) Go back
                """
                print(profile_options)
                option = get_user_option(1, 3)
                # option to view profile or create
                while option < 1 or option > 3:
                    print("Invalid selection")
                    option = get_user_option(1, 3)
                if option == 1:
                    view_profile()
                elif option == 2:
                    profile()
                    continue
                elif option == 3:
                    break
        elif option == 9:
            result = search_for_friend()
        elif option == 10:
            str = ""
            print("You have already connected with:")
            with open('database.json') as db:
                data = json.load(db)
                for user in data["users"]:
                    if user["username"] == LOGGED_IN_USER["username"]:
                        str = LOGGED_IN_USER["username"]
                        print('\n'.join(user["friends"]), )

                    yes_no = prompt(
                        "Would you like to disconnect from any of your friends?(y/n): ")
                    if yes_no == True:
                        deleted_friend = input(
                            "Enter the name of the friend you want to delete from the list above: ")
                        if deleted_friend in user["friends"]:
                            user["friends"].remove(deleted_friend)
                            print(deleted_friend, "was deleted")

                            with open('database.json', 'w+') as db:
                                json.dump(data, db)
                            for user in data["users"]:
                                if user["username"] == deleted_friend:
                                    user["friends"].remove(str)
                                    with open('database.json', 'w+') as db:
                                        json.dump(data, db)
                        else:
                            print(
                                "The username you entered is not part of your friends.")
                    else:
                        print("Going back to the main menu.")
                        break
        elif option == 11:
            friends = print_friends(LOGGED_IN_USER["username"])
            choice = int(input(
                f"Please enter the ID number of the friend you want to message ({1}-{len(friends)}). Enter 0 to go back to main menu: "))
            while choice < 0 or choice > len(friends):
                print("Invalid Input. Try again")
                choice = int(input(
                    f"Please enter the ID number of the friend you want to message ({1}-{len(friends)}). Enter 0 to go back to main menu: "))
            if choice == 0:
                continue
            message = input("Enter the message you want to send: ")
            sucess = send_message(friends[choice - 1], message)
        elif option == 12:
            view_inbox()
        elif option == 13:
            x = learning(username, 'database.json',new_training)
        elif option == 14:  # Logout
            exit()
