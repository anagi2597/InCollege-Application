from modules.learning import *
# 3 Ayman

def writeTraining(database="database.json"):
    data = load_db(database)

    # Clear file in case it already exists
    f = open("MyCollege_training.txt", "w")
    f.close()

    f = open("MyCollege_training.txt", "w")
    for user in data["users"]:
        if user.get("learning") == None: # No courses taken
            pass
        else:
            f.write(user["username"] + ":\n")
            if len(user["learning"]) == 0:
                f.write("\tNo courses taken yet.")
            else:
                for course in user["learning"]:
                    f.write("\t" + course)
            f.write("\n==========\n")
    f.close()