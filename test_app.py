# # This file contains all our pytest

# # Import every method/variable from our app file
from app import *
from modules.login_notifications import *
import json
import uuid
from modules.jobs2 import *
import sys
from modules.profile_view import *
from modules.learning import *
from API.savedJobs import *
from API.appliedJobs import *
from API.writeTraining import *
from API.userTier import *
from API.writeProfile import *
from API.api import *


print("Starting test")


def test_user_option():
    option = get_user_option(1, 3)
    assert isinstance(option, int)
    assert option <= 5 and option >= 1


def test_verify_password():
    acceptable_passwords = [
        "tahirMon@1",
        "hoanGngu@12",
        "joRgo(76"
    ]
    invalid_passwords = [
        "tahirMo",
        "hoangnguy@",
        "jorgoK76",
        "invalid",
        "inV#lid"
    ]

    for password in acceptable_passwords:
        assert verify_password(password) == True

    for password in invalid_passwords:
        assert verify_password(password) == False


# initializes empty database
with open("test_database.json", 'w+') as db:
    init_db = {
        "users": []
    }
    json.dump(init_db, db)
    db.close()


def test_login_and_register():
    valid_fake_users = [
        {"username": "newUser46", "password": "tahirMon@1",
         "first_name": "John", "last_name": "Cena", "plus_tier": True},
        {"username": "newUser47", "password": "hoanGngu@12",
         "first_name": "The", "last_name": "Rock", "plus_tier": False},
        {"username": "newUser48",
         "password": "joRgo(76", "first_name": "Elon", "last_name": "Musk", "plus_tier": False},
        {"username": "newUser49", "password": "newUser4@",
         "first_name": "Steve", "last_name": "Jobs", "plus_tier": True},
        {"username": "newUser50", "password": "newUser4$",
         "first_name": "Bill", "last_name": "Gates", "plus_tier": True},
    ]

    for user in valid_fake_users:
        assert verify_register(user["username"], user["password"], user["first_name"],
                               user["last_name"], user["plus_tier"], database="test_database.json") == True
        assert login(user["username"], user["password"],
                     database="test_database.json") == True  # verify_login

    # lets now delete user and test that we can't register a user that doesnt have unique username and first/last name
    with open("test_database.json", 'r') as db:
        data = json.load(db)
        db.close()

    with open("test_database.json", 'w+') as db:
        data["users"].pop()
        json.dump(data, db)
        db.close()

    for i in range(4):
        assert verify_register(valid_fake_users[i]["username"], valid_fake_users[i]["password"], valid_fake_users[i]
                               ["first_name"], valid_fake_users[i]["last_name"], valid_fake_users[i]["plus_tier"],
                               database="test_database.json") == False

    # Insert the user that was deleted so it is full again
    assert verify_register(valid_fake_users[4]["username"], valid_fake_users[4]["password"], valid_fake_users[4]
                           ["first_name"], valid_fake_users[4]["last_name"], valid_fake_users[i]["plus_tier"],
                           database="test_database.json") == True


def test_skills_options():
    options = list_of_skills()
    assert options[0] <= 6 and options[0] >= 1
    if options[0] == 1:
        assert options[1] == "1.) Programming"
    if options[0] == 2:
        assert options[1] == "2.) Carpentry"
    if options[0] == 3:
        assert options[1] == "3.) Photography"
    if options[0] == 4:
        assert options[1] == "4.) Microsoft Excel"
    if options[0] == 5:
        assert options[1] == "5.) Learn Spanish"
    if options[0] == 6:
        assert options[1] == "6.) Exit"


def test_post_job():
    valid_fake_jobs = [
        ["", "", "", "", ""],
        ["Mover", "Help clients move to new house",
         "Bulls Moving Co.", "Tampa, FL", 10],
        ["Developer", "Develop new state of the art software at our company!",
         "Apple", "San Francisco, CA", "hudred thousand dollars"],
        ["Professor", "None", "USF", "Tampa, FL", 80000],
        ["", "", "", "", ""],
        ["Mover", "Help clients move to new house",
         "Bulls Moving Co.", "Tampa, FL", 10],
        ["Developer", "Develop new state of the art software at our company!",
         "Apple", "San Francisco, CA", "hudred thousand dollars"],
        ["Professor", "None", "USF", "Tampa, FL", 80000],
    ]

    new_job = ["Janitor", "Clean the mess of the future generation of engineers",
               "USF", "Tampa, FL", "25 dollars an hours"]

    invalid_fake_jobs = [
        [None, "Help clients move to new house", "Bulls Moving Co.", None, 10],
        ["Professor", None, "USF", "Tampa, Fl", 80000],
        [None, "Clean the mess of the future generation of engineers",
         "USF", "Tampa, FL", None],
    ]

    # Test invalid jobs
    for i in range(len(invalid_fake_jobs)):
        assert post_job(invalid_fake_jobs[i][0], invalid_fake_jobs[i][1], invalid_fake_jobs[i][2],
                        invalid_fake_jobs[i][3], invalid_fake_jobs[i][4], database="test_database.json") == [False, 500]

    # Login each user to Test valid job postings
    with open("test_database.json", "r") as db:
        data = json.load(db)
        db.close()

    i = 0
    for user in data["users"]:
        login(user["username"], user["password"],
              database="test_database.json")

        if i == 10:  # Test limit of 10 jobs
            assert post_job(new_job[0], new_job[1], new_job[2], new_job[3],
                            new_job[4], database="test_database.json") == [False, 404]
        else:  # Test valid jobs
            assert post_job(valid_fake_jobs[i][0], valid_fake_jobs[i][1], valid_fake_jobs[i][2],
                            valid_fake_jobs[i][3], valid_fake_jobs[i][4], database="test_database.json") == [True, 200]
        i += 1


def test_find_user():
    valid_fake_users = [
        {"username": "newUser46", "password": "tahirMon@1",
         "first_name": "John", "last_name": "Cena"},
        {"username": "newUser47", "password": "hoanGngu@12",
         "first_name": "The", "last_name": "Rock"},
        {"username": "newUser48",
         "password": "joRgo(76", "first_name": "Elon", "last_name": "Musk"},
        {"username": "newUser49", "password": "newUser4@",
         "first_name": "Steve", "last_name": "Jobs"},
        {"username": "newUser50", "password": "newUser4$",
         "first_name": "Bill", "last_name": "Gates"},
    ]

    invalid_fake_users = [
        {"username": "newUser44", "password": "tahirM3on@1",
         "first_name": "Johns", "last_name": "Qen"},
        {"username": "newUser42", "password": "hoanGn3gu@12",
         "first_name": "Thes", "last_name": "Rocky"},
        {"username": "newUser41",
         "password": "joRgo2(76", "first_name": "Elona", "last_name": "Musq"},
        {"username": "newUser4", "password": "newUser14@",
         "first_name": "Steven", "last_name": "Job"},
        {"username": "newUser510", "password": "newU1ser4$",
         "first_name": "Billy", "last_name": "Gate"},
    ]

    for user in invalid_fake_users:
        assert find_user(user["first_name"], user["last_name"],
                         database="test_database.json") == False

    with open("test_database.json", "r") as db:
        data = json.load(db)
        db.close()

    for user in data["users"]:
        assert find_user(user["first_name"], user["last_name"],
                         database="test_database.json") == True


def test_useful_links():
    ### CANNOT TEST SIGNUP OPTION, WILL FAIL BECAUSE OF EXTRA NEEDED INPUT ###

    # Delete a user if database is full to test the sign up option
    # with open("database.json", 'r') as db:
    #         data = json.load(db)
    #         db.close()

    # with open("database.json", 'w+') as db:
    #         data["users"].pop()
    #         json.dump(data, db)
    #         db.close()

    options = print_useful_links()
    if options == 1:
        assert options == """
                            --Available Options--
                            1.) Sign Up
                            2.) Help Center
                            3.) About
                            4.) Press
                            5.) Blog
                            6.) Careers
                            7.) Developers
                            8.) Go Back
                            """
        # Not sure how to test the signup option
        # if options == 1:
        #     assert options == True
        if options == 2:
            assert options == "We're here to help"
        if options == 3:
            assert options == "InCollege: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide"
        if options == 4:
            assert options == "InCollege Pressroom: Stay on top of the latest news, updates, and reports"
        if options == 5:
            assert options == "Under Construction"
        if options == 6:
            assert options == "Under Construction"
        if options == 7:
            assert options == "Under Construction"
        if options == 8:
            assert options == False  # "Going back to 'Useful Links' Menu"
    if options == 2:
        assert options == "Under Construction"
    if options == 3:
        assert options == "Under Construction"
    if options == 4:
        assert options == "Under Construction"
    if options == 5:
        assert options == False

    # Tried to test automatic input for signup but tests kept failing, tried nested mocks but still failed
    # with mock.patch.object(builtins, 'input', lambda _: 1):
    #      assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: '1'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: 'Bernie'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: 'Sanders'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: 'Sandman'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: "S@ndm@n69*"):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: '8'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: '5'):
    #     assert print_useful_links() == False


def test_privacy_policy():
    # empty the database
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    fake_user = {"username": "newUser46", "password": "tahirMon@1",
                 "first_name": "John", "last_name": "Cena", "plus_tier": False}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], fake_user["plus_tier"],
                           "test_database.json") == True
    LOGGED_IN_USER
    assert login(fake_user["username"],
                 fake_user["password"], "test_database.json") == True
    assert toggle_privacy(
        LOGGED_IN_USER["username"], "test_database.json") == True
    with open("test_database.json", "r") as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                assert isinstance(user["settings"]["email"], bool)
                assert isinstance(user["settings"]["sms"], bool)
                assert isinstance(user["settings"]["targeted_ads"], bool)
                assert isinstance(user["settings"]["language"], str)

                assert user["settings"]["email"] == False or user["settings"]["email"] == True
                assert user["settings"]["sms"] == False or user["settings"]["sms"] == True
                assert user["settings"]["targeted_ads"] == False or user["settings"]["targeted_ads"] == True
                assert user["settings"]["language"] == "English" or user["settings"]["language"] == "Spanish"
        db.close()


def test_upper_case_func():
    lowercase_majors = [
        "Computer science",
        "computer engineering",
        "biology",
        "chemical engineering",
        "fake major with five words"
    ]
    assert upper_case(lowercase_majors[0]) == "Computer Science"
    assert upper_case(lowercase_majors[1]) == "Computer Engineering"
    assert upper_case(lowercase_majors[2]) == "Biology"
    assert upper_case(lowercase_majors[3]) == "Chemical Engineering"
    assert upper_case(lowercase_majors[4]) == "Fake Major With Five Words"


def test_creating_profile():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    profile_1 = {
        "title": "Senior",
        "major": upper_case("computer science"),
        "university": upper_case("university of south florida"),
        "about": "test friend",
        "experience": [
            {
                "title": "Customer relation director",
                "employer": "Burgerking",
                "date_started": "6/9/2006",
                "date_ended": "6/9/2009",
                "location": "Tampa",
                "description": "Handle and fulfill customer's request"
            }
        ],
        "education": [
            {
                "school": "USF",
                "degree": "Undergrad",
                "years_att": "2069"
            }
        ]
    }
    fake_user = {"username": "newUser46", "password": "tahirMon@1",
                 "first_name": "John", "last_name": "Cena", "plus_tier": True}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], fake_user["plus_tier"],
                           "test_database.json") == True
    LOGGED_IN_USER
    assert login(fake_user["username"],
                 fake_user["password"], "test_database.json") == True
    assert post_title(profile_1["title"], profile_1["major"], profile_1["university"], profile_1["about"],
                      profile_1["experience"], profile_1["education"], "test_database.json")[0] == True
    with open("test_database.json", 'r') as db:
        data = json.load(db)
        for user in data["users"]:
            if user.get("posted_title"):  # Only verify is user has created a profile
                # Verify major is capitalized
                major = user["posted_title"]["major"].split()
                assert (x.isupper() for x in major)

                # Verify university is capatilized
                university = user["posted_title"]["university"].split()
                assert (x.isupper() for x in university)

                # Verify experience is more than 3
                experience_length = len(user["posted_title"]["experience"])
                assert experience_length >= 0 and experience_length <= 3


def test_profile_view():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    profile_1 = {
        "title": "Senior",
        "major": "Computer Science",
        "university": "USF",
        "about": "test 2",
        "experience": [
            {
                "title": "Customer relation director",
                "employer": "McDonald's",
                "date_started": "6/9/2006",
                "date_ended": "6/9/2009",
                "location": "Tampa",
                "description": "Handle and fulfill customer's request"
            }
        ],
        "education": [
            {
                "school": "USF",
                "degree": "Undergrad",
                "years_att": "2020"
            }
        ]
    }
    profile_2 = {
        "title": "Senior",
        "major": "Computer Science",
        "university": "USF",
        "about": "test 2",
        "experience": [
            {
                "title": "Customer relation director",
                "employer": "McDonald's",
                "date_started": "6/9/2006",
                "date_ended": "6/9/2009",
                "location": "Tampa",
                "description": "Handle and fulfill customer's request"
            }
        ],
        "education": [
            {
                "school": "USF",
                "degree": "Undergrad",
                "years_att": "2020"
            }
        ]
    }
    fake_user = {"username": "alexm", "password": "Alex123!",
                 "first_name": "Alex", "last_name": "Miller", "plus_tier": True}
    fake_friend = {"username": "ayman", "password": "Ayman123!",
                   "first_name": "Ayman", "last_name": "Nagi", "plus_tier": True}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], fake_user["plus_tier"],
                           "test_database.json") == True

    display_user(fake_user["username"])

    friend_option()

    options = get_user_option(1, 2)
    if options == 1:
        print("No friends listed")
    if options == 2:
        assert options == 2


def test_friend_list():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    fake_user = {"username": "alexm", "password": "Alex123!",
                 "first_name": "Alex", "last_name": "Miller", "plus_tier": False}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], fake_user["plus_tier"],
                           "test_database.json") == True
    str = ""
    print("You have already connected with:")
    with open('test_database.json') as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                str = LOGGED_IN_USER["username"]
                print('\n'.join(user["friends"]), )

            yes_no = prompt(
                "Would you like to disconnect from any of your friends?(y/n): ")
            if yes_no:
                deleted_friend = input(
                    "Enter the name of the friend you want to delete from the list above: ")
                if deleted_friend in user["friends"]:
                    user["friends"].remove(deleted_friend)
                    print(deleted_friend, "was deleted")

                    with open('test_database.json', 'w+') as db:
                        json.dump(data, db)
                    for user in data["users"]:
                        if user["username"] == deleted_friend:
                            user["friends"].remove(str)
                            with open('test_database.json', 'w+') as db:
                                json.dump(data, db)
                else:
                    print("The username you entered is not part of your friends.")
            else:
                break


def test_friend_search():
    username = input("Please enter a username (type in 'alexm' for test): ")
    password = input(
        "Please enter a password (type in 'Alexm123!' for test) : ")
    logged_in = login(username, password)

    friend = str(
        input(
            "Search for people you know by last name, university, or their major (type in last name 'Nagi' for test case): "))
    people_found = []
    found_friend = False

    # Search db for friend by last name, university, or major
    with open("database.json", 'r') as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                continue
            if user["last_name"] == friend:
                people_found.append(user["username"])
                found_friend = True
        db.close()

    if found_friend:
        i = 1
        print("We found " + str(len(people_found)) +
              " person(s) that matched your search. Please select your friend:")
        print("0. Exit")
        # Print all people with matching results
        for name in people_found:
            print(str(i) + ". " + str(name))
            i += 1
        # Let user select friend to add and make pending request for friend
        selection = get_user_option(0, len(people_found))
        if selection == 0:  # If they select exit
            return False
        else:  # If selected a person to add
            selection -= 1
            request_friend(people_found[selection], LOGGED_IN_USER["username"])
            print("You have successfully sent " +
                  str(people_found[selection]) + " a friend request.")
            return True
    else:
        print("Sorry we couldn't find your friend")
        return False


def test_del_job():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        # data = json.load(db)
        db.close()

    fake_user = {"username": "alexm", "password": "Alex123!",
                 "first_name": "Alex", "last_name": "Miller", "plus_tier": True}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], fake_user["plus_tier"],
                           "test_database.json") == True
    logged_in = login("alexm", "Alexm123!")
    while True:
        time.sleep(1)
        print_manage_jobs()
        user_choice = get_user_option(1, 5)
        while user_choice < 1 or user_choice > 5:
            print("Invalid input. Try again")
            user_choice = get_user_option(1, 5)
        if user_choice == 1:  # Delete a job
            deleted = delete_job()
            assert deleted == True
            return True
        elif user_choice == 2:  # View saved jobs
            edit_saved = edit_saved_jobs()
            assert edit_saved == True
            return True
        elif user_choice == 3:  # View applied jobs
            printApplied = print_applied_jobs()
            assert printApplied == True
            return True
        elif user_choice == 4:  # View jobs not applied for
            notApplied = print_not_applied()
            assert notApplied == True
            return True
        else:
            break


"""
def test_get_all_jobs():
    user_object={"username": "Star", "password": "Star123!", "first_name": "Star", "last_name": "Jones",posted_jobs=[{
    "job_id": "11111111-14a4-11eb-9bec-ed7ef134cb3d", "title": "Singer", "description": "Singing as a second voice with the band called Blue", "employer": "Blue", "location": "London", "salary": "111,111"
    },
    {
        "job_id": "22222222-14a4-11eb-9bec-ed7ef134cb3d", "title": "Dj",
        "description": "Perform in a night club as an EDM Dj", "employer": "Ybor Club", "location": "Tampa",
        "salary": "55,555"
    }]}
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        users.append(user_object)
        json.dump(init_db, db)
        db.close()
    with open("test_database.json", "r") as db:
        list=get_all_jobs('test_database.json')
        assert list["job_id"]="11111111-14a4-11eb-9bec-ed7ef134cb3d" return True
        assert list["jod_id"]="22222222-14a4-11eb-9bec-ed7ef134cb3d" return True

def test_save_job():
    with open('test_database.json, 'r+') as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:

                job_saved={"job_id": "22222222-14a4-11eb-9bec-ed7ef134cb3d", "title": "Dj",
                "description": "Perform in a night club as an EDM Dj", "employer": "Ybor Club", "location": "Tampa",
                "salary": "55,555"}
                save_job(job_saved)
                assert user["saved_jobs"]="22222222-14a4-11eb-9bec-ed7ef134cb3d"
"""


# Epic 7


def test_print_friends():
    # Clear DB
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()

    valid_fake_users = [
        {"username": "newUser46", "password": "tahirMon@1",
         "first_name": "John", "last_name": "Cena", "plus_tier": False,
         "friends": ["newUser47", "newUser48", "newUser49", "newUser50"], "inbox": []},
        {"username": "newUser47", "password": "hoanGngu@12",
         "first_name": "The", "last_name": "Rock", "plus_tier": False,
         "friends": ["newUser46", "newUser48", "newUser49"]},

        {"username": "newUser48",
         "password": "joRgo(76", "first_name": "Elon", "last_name": "Musk", "plus_tier": True,
         "friends": ["newUser50"]},

        {"username": "newUser49", "password": "newUser4@",
         "first_name": "Steve", "last_name": "Jobs", "plus_tier": True,
         "friends": ["newUser46", "newUser47", "newUser48", "newUser50", ]},

        {"username": "newUser50", "password": "newUser4$",
         "first_name": "Bill", "last_name": "Gates", "plus_tier": False, "friends": ["newUser47", "newUser48"]},
    ]

    # Insert valid fake users with already listed friends
    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'w+') as db:
        for user in valid_fake_users:
            data["users"].append(user)
        json.dump(data, db)
        db.close()

    # Test the print_friends function on valid_fake users
    for VFuser in valid_fake_users:
        # Login each user for it to work
        logging = login(VFuser["username"], VFuser["password"],
                        database="test_database.json")
        # lists should be equal
        assert print_friends(
            LOGGED_IN_USER["username"], database="test_database.json") == VFuser["friends"]


def test_send_message():
    with open("test_database.json") as db:
        data = json.load(db)

        default_recipient = "newUser46"  # The user that everyone will send a message to
        default_message = "Hello!"

        for user in data["users"]:
            if user["username"] == default_recipient:  # Don't send message to self
                continue

            logging = login(user["username"], user["password"],
                            database="test_database.json")

            # If they are friends they can send messages regardless of tier
            if default_recipient in user["friends"]:
                assert send_message(
                    default_recipient, default_message, database="test_database.json") == True
            # "Plus" members can send messages regardless of if they are friends or not
            elif user["plus_tier"] == True:
                assert send_message(
                    default_recipient, default_message, database="test_database.json") == True
            else:  # Not friends and user is not a "plus" member
                assert send_message(
                    default_recipient, default_message, database="test_database.json") == False
        db.close()


def test_has_inbox():
    # Clear DB
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()

    valid_fake_users = [
        {"username": "newUser46", "password": "tahirMon@1",
         "first_name": "John", "last_name": "Cena", "plus_tier": False,
         "friends": ["newUser47", "newUser48", "newUser49", "newUser50"],
         "inbox": [{"From": "newUser48", "Message": "Hello!", "isNew": True},
                   {"From": "newUser49", "Message": "Hello!", "isNew": True}]},

        {"username": "newUser47", "password": "hoanGngu@12",
         "first_name": "The", "last_name": "Rock", "plus_tier": False,
         "friends": ["newUser46", "newUser48", "newUser49"],
         "inbox": [{"From": "newUser48", "Message": "Hello!", "isNew": True},
                   {"From": "newUser49", "Message": "Hello!", "isNew": True}]},

        {"username": "newUser48",
         "password": "joRgo(76", "first_name": "Elon", "last_name": "Musk", "plus_tier": True, "friends": ["newUser50"],
         "inbox": []},

        {"username": "newUser49", "password": "newUser4@",
         "first_name": "Steve", "last_name": "Jobs", "plus_tier": True,
         "friends": ["newUser46", "newUser47", "newUser48", "newUser50"], "inbox": []},

        {"username": "newUser50", "password": "newUser4$",
         "first_name": "Bill", "last_name": "Gates", "plus_tier": False, "friends": ["newUser46", "newUser48"],
         "inbox": []},
    ]

    # Insert valid fake users with already listed friends
    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'w+') as db:
        for user in valid_fake_users:
            data["users"].append(user)
        json.dump(data, db)
        db.close()

    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'r') as db:
        for user in data["users"]:
            logging = login(user["username"], user["password"],
                            database="test_database.json")
            if user["username"] == LOGGED_IN_USER["username"]:
                if user["inbox"] == []:
                    assert has_inbox(database="test_database.json") == False
                else:
                    assert has_inbox(database="test_database.json") == True
        db.close()


def test_check_last_applied():
    # Clear DB
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()

    # User to test the last_applied date, data is one month old as of writing
    fake_user = {"username": "newUser46", "password": "tahirMon@1",
                 "first_name": "John", "last_name": "Cena", "last_applied": "10 09 2020", "new_reg": [],
                 "applied_jobs": ["b34ecbbc-1325-11eb-bf1f-367dda070ab5"]}

    # Insert valid fake users with already listed friends
    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'w+') as db:
        data["users"].append(fake_user)
        json.dump(data, db)
        db.close()

    logging = login(
        fake_user["username"], fake_user["password"], database="test_database.json")

    # Void function so can't assert anything
    # If notifaction prints then we know it is working correctly
    check_last_applied(database="test_database.json")


def test_check_new_reg():
    # Clear DB
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()

    # User already in test_database
    old_fake_user = {"username": "newUser46", "password": "tahirMon@1",
                     "first_name": "John", "last_name": "Cena", "last_applied": "10 09 2020", "new_reg": [],
                     "applied_jobs": ["b34ecbbc-1325-11eb-bf1f-367dda070ab5"]}

    # User to test the new registration notification
    new_fake_user = {"username": "newUser47", "password": "hoanGngu@12",
                     "first_name": "The", "last_name": "Rock", "new_reg": [],
                     "applied_jobs": ["b34ecbbc-1325-11eb-bf1f-367dda070ab5"]}

    # Register new user to test if notification of new user works
    verify_register(new_fake_user["username"], new_fake_user["password"], new_fake_user["first_name"],
                    new_fake_user["last_name"], True, database="test_database.json")

    # Login in old user so they will get the notification of a new regitration
    logging = login(
        old_fake_user["username"], old_fake_user["password"], database="test_database.json")

    # Test that registering new user added the new user to existing users' new_reg[]
    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                assert len(user["new_reg"]) == 1
                break
        db.close()

    # Void function, if notification prints we know it works correctly
    check_new_reg(database="test_database.json")

    # Test that after check_new_reg() is run the new user is popped from new_reg[] so they don't get notified of the same user twice
    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                assert len(user["new_reg"]) == 0
                break
        db.close()


def test_buf_delete_job_and_check_delete_job():
    # Clear DB
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()

    # User to test the last_applied date, data is one month old as of writing
    fake_users = [
        {"username": "newUser46", "password": "tahirMon@1",
         "first_name": "John", "last_name": "Cena", "last_applied": "10 09 2020", "new_reg": [],
         "applied_jobs": ["b34ecbbc-1325-11eb-bf1f-367dda070ab5"], "job_del": []},
        {"username": "newUser47", "password": "hoanGngu@12",
         "first_name": "The", "last_name": "Rock", "new_reg": [],
         "applied_jobs": ["b34ecbbc-1325-11eb-bf1f-367dda070ab5"], "job_del": []}
    ]

    # Insert fake users with already listed friends
    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'w+') as db:
        for user in fake_users:
            data["users"].append(user)
        json.dump(data, db)
        db.close()

    job_to_delete = {"title": "Help Wanted", "description": "Looking for help", "employer": "Ayman",
                     "location": "Tampa", "salary": "69", "job_id": "b34ecbbc-1325-11eb-bf1f-367dda070ab5"}

    # Delete the above job from both users' applied_jobs list
    buf_delete_job(job_to_delete, database="test_database.json")

    # Test that the jobs were removed from applied_jobs lists and added to jobs_del
    # Also test that the notification will print for each user
    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'r') as db:
        for user in data["users"]:
            assert len(user["applied_jobs"]) == 0
            assert len(user["job_del"]) == 1

            logging = login(user["username"], user["password"],
                            database="test_database.json")

            # Void function should print notification that the job was deleted
            check_delete_job(database="test_database.json")

        db.close()

    with open("test_database.json") as db:
        data = json.load(db)
    with open("test_database.json", 'r') as db:
        for user in data["users"]:
            # Make sure that the job was removed so we aren't reminded twice
            assert len(user["job_del"]) == 0
        db.close()


def test_profile_notification():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()

    mock_users = [{
        "username": "tahirM",
        "password": "tahirM@123",
        "first_name": "Tahir",
        "last_name": "Montgomery",
        "tier": 2
    }, {
        "username": "donaldTrump",
        "password": "orAnge@123",
        "first_name": "Donald",
        "last_name": "Trump",
        "tier": 2
    }, {
        "username": "joeBiden",
        "password": "sleepY@123",
        "first_name": "Joe",
        "last_name": "Biden",
        "tier": 2
    }]

    for user in mock_users:
        assert (verify_register(user["username"], user["password"], user["first_name"],
                                user["last_name"], user["tier"], "test_database.json") == True)

    with open("test_database.json", "r") as db:
        data = json.load(db)
        db.close()

    with open("test_database.json", "w+") as db:
        for user in data["users"]:
            user["posted_title"] = {}
        json.dump(data, db)
        db.close()

    # assert that the 'Don't forget to create a profile.' message isnt printed
    for user in data["users"]:
        assert (login(user["username"], user["password"],
                      "test_database.json") == True)
        message = profile_notification("test_database.json")
        assert (message == "Don't forget to create a profile.")

    with open("test_database.json", "w+") as db:
        for user in data["users"]:
            user["posted_title"] = {
                "title": "Not empty"
            }
        json.dump(data, db)
        db.close()

    # assert that the 'Profile Created' message isnt printed
    for user in data["users"]:
        assert (login(user["username"], user["password"],
                      "test_database.json")) == True
        message = profile_notification("test_database.json")
        assert (message == None)


def test_number_of_applied_jobs():
    with open("test_database.json", "r") as db:
        data = json.load(db)
        db.close()

    with open("test_database.json", "w+") as db:
        count = 1
        for user in data["users"]:
            for i in range(count):
                user["applied_jobs"].append(str(uuid.uuid1()))
            count += 1
        json.dump(data, db)
        db.close()

    for user in data["users"]:
        assert (login(user["username"], user["password"],
                      "test_database.json")) == True
        assert (len(user["applied_jobs"]) ==
                applied_for_jobs("test_database.json"))


def test_new_jobs_notification():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()

    mock_users = [{
        "username": "tahirM",
        "password": "tahirM@123",
        "first_name": "Tahir",
        "last_name": "Montgomery",
        "tier": 2
    }, {
        "username": "donaldTrump",
        "password": "orAnge@123",
        "first_name": "Donald",
        "last_name": "Trump",
        "tier": 2
    }, {
        "username": "joeBiden",
        "password": "sleepY@123",
        "first_name": "Joe",
        "last_name": "Biden",
        "tier": 2
    }]

    for user in mock_users:
        assert (verify_register(user["username"], user["password"], user["first_name"],
                                user["last_name"], user["tier"], "test_database.json")) == True

    with open("test_database.json", "r") as db:
        data = json.load(db)
        db.close()

    with open("test_database.json", "w+") as db:
        count = 0
        for user in data["users"]:
            user["posted_jobs"].append({
                "title": f"Fake Job {count + 1}"
            })
            user["posted_jobs"].append({
                "title": f"Fake Job {count + 2}"
            })
            user["posted_jobs"].append({
                "title": f"Fake Job {count + 3}"
            })
            count += 3
        json.dump(data, db)
        db.close()
    for user in data["users"]:
        assert (login(user["username"], user["password"],
                      "test_database.json")) == True
        jobs = get_all_jobs("test_database.json")
        assert (new_jobs_notification(jobs) == True)


def test_training_options():
    while True:
        # print_welcome3()
        option = get_user_option(1, 7)
        while option < 1 or option > 7:
            print("Invalid input. Try again")
            option = get_user_option(1, 7)
        if option == 1:  # Login
            print("Choose option 6 to test taining options")
            continue
        elif option == 2:  # Create new account
            print("Choose option 6 to test taining options")
            continue
        elif option == 3:
            print("Choose option 6 to test taining options")
            continue
        elif option == 4:
            print("Choose option 6 to test taining options")
            continue
        elif option == 5:  # Watch Video
            print("Choose option 6 to test taining options")
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
        else:
            return False


def test_course_learning():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    user = {
        "username": "tahirm",
        "password": "tahirM123@",
        "first_name": "Tahir",
        "last_name": "Montgomery",
        "tier": 2
    }
    assert (verify_register(user["username"], user["password"], user["first_name"],
                            user["last_name"], user["tier"], "test_database.json") == True)
    assert (login(user["username"], user["password"],
                  "test_database.json") == True)

    count = 0
    cours=["How to code", "How to be successful", "How to live healthy"]
    
    learning(user["username"], "test_database.json", cours)



def test_saved_jobs(database="database.json"):
    allJobs = getAllJobs(database)
    data = load_db(database)

    # Clear file if already exists
    f = open("MyCollege_savedJobs.txt", "w")
    f.close()

    f = open("MyCollege_savedJobs.txt", "a")

    for user in data["users"]:
        if len(user["saved_jobs"]) >= 1:  # If they have at least one saved job
            f.write(user["username"] + ": ")
            for jobID in user["saved_jobs"]:  # saved_jobs only stores IDs
                for job in allJobs:  # Search all jobs to match jobID to job title
                    # Last Job, dont add comma to end
                    if jobID == user["saved_jobs"][-1] and jobID == job["job_id"]:
                        f.write(job["title"])
                    elif jobID == job["job_id"]:
                        f.write(job["title"] + ",\t")
            f.write("\n==========\n")

    print("All Saved Jobs were outputted to MyCollege_savedJobs.txt")
    f.close()


def test_applied_jobs(database="database.json"):
    allJobs = getAllJobs(database)
    data = load_db(database)

    # Clear file if already exists
    f = open("MyCollege_appliedJobs.txt", "w")
    f.close()

    f = open("MyCollege_appliedJobs.txt", "a")
    printName = 0

    for job in allJobs:
        f.write(job["title"] + ":\n")
        for user in data["users"]:
            printName = 0
            if len(user["applied_jobs"]) >= 1:  # If they have at least one applied job
                for jobID in user["applied_jobs"]:
                    if jobID["job"] == job["job_id"]:
                        if printName == 0:
                            f.write("\t" + user["username"] + ": ")
                            printName = 1
                        f.write(jobID["user_description"] + "\n")
        f.write("==========\n")
    print("All jobs applied for were outputted to MyCollege_appliedJobs.txt")
    f.close()


def test_training(database="database.json"):
    data = load_db(database)

    # Clear file in case it already exists
    f = open("MyCollege_training.txt", "w")
    f.close()

    f = open("MyCollege_training.txt", "w")
    for user in data["users"]:
        if user.get("learning") == None:  # No courses taken
            pass
        else:
            f.write(user["username"] + ":\n")
            if len(user["learning"]) == 0:
                f.write("\tNo courses taken yet.")
            else:
                for course in user["learning"]:
                    f.write("\t" + course)
            f.write("\n==========\n")
    print("Training courses taken by all users were outputted to MyCollege_training.txt")
    f.close()


def test_users(database="database.json"):
    with open(database, "r") as db:
        data = json.load(db)
        db.close()

    # CLear file
    f = open("MyCollege_users.txt", "w")
    f.close

    f = open("MyCollege_users.txt", "w")

    for user in data["users"]:
        f.write("Username: " + user["username"] + "\nStatus: ")
        if user["plus_tier"] == True:
            f.write("Plus")
        else:
            f.write("Standard")
        f.write("\n==========\n")
    print("List of all usernames outputted to MyCollege_users.txt")
    f.close()


def test_api_writeJobs(database="database.json"):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()

    f = open("MyCollege_jobs.txt", "w")
    f.close()

    f = open("MyCollege_jobs.txt", "w")
    allJobs = getAllJobs(database)
    for job in allJobs:
        f.write(job["title"])
        f.write("\n")
        f.write(job["description"])
        f.write("\n")
        f.write(job["employer"])
        f.write("\n")
        f.write(job["location"])
        f.write("\n")
        f.write(job["salary"])
        f.write("\n==========\n")
    f.close()


def test_user_profiles(database="database.json"):
    with open(database, "r") as db:
        data = json.load(db)
        db.close()

    # CLear file
    f = open("MyCollege_profiles.txt", "w")
    f.close

    f = open("MyCollege_profiles.txt", "w")

    # Save original stdout to print to terminal/screen
    original_stdout = sys.stdout

    # overwrite stdout to f so profile will print to the desired file
    sys.stdout = f

    for user in data["users"]:
        if user.get("posted_title") == None:  # No courses taken
            pass
        else:
            LOGGED_IN_USER = user
            display_user(user["username"])
        f.write("\n==========\n")
    f.close()

    # set stdout back to normal
    sys.stdout = original_stdout
    print("All profiles in the InCollege system were ouputted to MyCollege_profiles.txt")


def test_api_account(database="database.json"):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()
    val = api_account()
    with open(database) as db:
        datanew = json.load(db)
        if len(datanew["users"]) >= 10:
            assert val == False
        else:
            if len(datanew["users"]) >= len(data["users"]):
                pass
            else:
                assert val == False


def test_api_newJobs(database="database.json"):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()
    api_newJobs()
    countold = 0
    countnew = 0
    with open(database, 'r') as db:
        datanew = json.load(db)
        db.close()
    for user in datanew["users"]:
        if user["username"] == 'Obama':
            countnew = len(user["posted_jobs"])
    for user in data["users"]:
        if user["username"] == 'Obama':
            countold = len(user["posted_jobs"])

    if countnew >= countold:
        pass
    else:
        assert False


def test_api_training(database="database.json"):
    try:
        with open('newtraining.txt') as f:
            data = f.read().splitlines()
    except IOError:
        print("newtraining.txt does not exist")
        pass
    out = api_training()
    assert data == out
