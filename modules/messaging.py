import json
import time
from modules.login import LOGGED_IN_USER


def print_friends(username, database="database.json"):
    with open(database) as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                for index, friend in enumerate(user["friends"]):
                    print(f"ID {index + 1}.): {friend} ")
                return user["friends"]

def send_message(username, message, database="database.json"):
    with open(database) as db:
        data = json.load(db)

    with open(database, 'w+') as db:
        found_friend = False
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                if user["plus_tier"] == True:
                    found_friend = True
                for friend in user["friends"]:
                    if friend == username:
                        found_friend = True
        if found_friend:
            for user in data["users"]:
                if user["username"] == username:
                    if not user.get("inbox", None):
                        user["inbox"] = []

                    user["inbox"].append({
                        "From": LOGGED_IN_USER["username"],
                        "Message": message,
                        "isNew": True,
                    })
                    json.dump(data, db)
                    db.close()
                    return True
            print("User was not found")
        else:
            print("I'm sorry, you are not friends with that person")
            return False

        return False
