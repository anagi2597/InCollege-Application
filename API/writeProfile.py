import json
import sys
from modules.profile_view import *
#5 Ayman

def writeProfile(database="database.json"):
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
        if user.get("posted_title") == None: # No courses taken
            pass
        else:
            LOGGED_IN_USER = user
            display_user(user["username"])
        f.write("\n==========\n")
    f.close()

    # set stdout back to normal
    sys.stdout = original_stdout 
