import json
import time
from modules.login import LOGGED_IN_USER

# notifies user to create a profile when they sign in if they havent already


def profile_notification(database="database.json"):
    with open(database) as db:
        data = json.load(db)

    with open(database, 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                if user["posted_title"] == {}:
                    print("Don't forget to create a profile.")
                    time.sleep(2)
                    db.close()
                    return "Don't forget to create a profile."
                else:
                    continue

# notifies user how many jobs they have applied for when choosing "Search for a job" or "Manage jobs"


def applied_for_jobs(database="database.json"):

    count = 0

    with open(database) as db:
        data = json.load(db)

    with open(database, 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                for index, jobs in enumerate(user["applied_jobs"]):
                    count += 1
                print("You have currently applied for " + str(count) + " jobs.")
                return count


def new_job_notification(database="database.json"):
    with open(database) as db:
        data = json.load(db)

    with open(database, 'r') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                print("hi")

# notifies user of a new job posting that are not part of the original 6 posted jobs


def new_jobs_notification(jobs):
    count = 0
    for index, job in enumerate(jobs):
        count += 1
        title = job["title"]

        if count > 6:
            print("A new job <" + str(job["title"]) + "> has been posted.")
            time.sleep(1)
        else:
            continue
    return True
