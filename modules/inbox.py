import json
import time
from modules.login import LOGGED_IN_USER
from modules.messaging import send_message

def has_inbox(database="database.json"):
    with open(database) as db:
        data = json.load(db)

    with open(database, 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                if user["inbox"] == []:
                    print("Nothing in inbox")
                    time.sleep(2)
                    return False
                else:
                    for inbox_messages in user["inbox"]:
                        if inbox_messages["isNew"] == True:
                            print("You have messages waiting for you!")
                            time.sleep(3)
                            return True


def view_inbox(database="database.json"):
    with open(database) as db:
        data = json.load(db)

    with open(database, 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                    index = 0
                    counter = 1
                    for inbox_messages in user["inbox"]:
                        print("\n" + str(counter) + ")" + " From: " + str(inbox_messages["From"]) + " - " + str(inbox_messages["Message"]))
                        counter += 1

                        response = input("Would you like to respond to this message? (1 for Yes, 0 for No): ")

                        if response == "1":
                            message = input("Enter the response you want to send: ")
                            success = send_message(inbox_messages["From"], message)
                            print("Message sent!")
                            time.sleep(1)
                        else:
                            print("No response sent")

                        remove_message = input("Would you like to delete this message? (1 for Yes, 0 for No): ")

                        if remove_message == "1":
                            with open(database, 'w+') as db:
                                user["inbox"].pop(index)
                                json.dump(data,db)
                                print("Message deleted. View inbox to see if there are more messages.")
                                time.sleep(1)
                        continue


