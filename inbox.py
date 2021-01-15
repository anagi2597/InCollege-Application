import json
import time
from modules.login import LOGGED_IN_USER

def has_inbox():
    with open(database) as db:
        data = json.load(db)

    with open(database, 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                for message in user["inbox"]:
                    if isNew == True
                        print("New Message")