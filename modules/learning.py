import time
import json
from modules.login import *
#the whole function is brand new from epic 9 to 10. had to implement the APIs in some way..

def load_db(database="database.json"):
    try:
        with open(database, 'r+') as db:
            return json.load(db)
    except Exception as e:
        raise e


def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


def prompt(message):
    while True:
        choice = input(message).lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Please enter y or n")

#def post_course(course):
def learning(user_name, database, arr):

    with open(database, 'r+') as db:
        data = json.load(db)
        db.close()

    with open(database, 'w+') as db:
        for user in data["users"]:
            if user.get("learning") == None:
                user["learning"] = []
        json.dump(data, db)
        db.close()
    cours={"How to use In College learning":"Not Taken",
           "Train the trainer":"Not Taken",
           "Gamification of learning":"Not Taken",
          "Understanding the Architectural Design Process":"Not Taken",
           "Project Management Simplified":"Not Taken"
        }
    
    if arr:
        for i in range(0,len(arr)):
            cours[arr[i]]="Not Taken"

    with open(database) as db:
        data = json.load(db)
    for user in data["users"]:
        if user_name == user["username"]:
            training = user["learning"]
    for i in training:
        cours[i]="Taken"
    print("Courses that you can take(Courses that you have already taken are marked as 'Taken'):\n")
    for key in cours:
        print(key, ' : ', cours[key])


    opt=input("Enter the course you want to take(Pay attention to the capitals. The course has to be exacly as it is shown):")
    if opt in cours:
        if cours[opt]=="Taken":
            yes_no = prompt(
                "You have already taken this course, do you want to take it again?(y/n)")
            if yes_no==True:
                print("You have now completed this training")
            else:
                print("Course Cancelled")
        if cours[opt]=="Not Taken":
            with open(database, 'w+') as db:
                for user in data["users"]:
                    if user["username"] == LOGGED_IN_USER["username"]:
                        user["learning"].append(opt)
                json.dump(data, db)
                db.close()
                print("You have now completed this training")
    else:
        print("Course not in the list of available courses. Try again")
