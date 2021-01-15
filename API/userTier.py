import json
#4 Ayman

def writeTiers(database="database.json"):
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
    f.close()
    