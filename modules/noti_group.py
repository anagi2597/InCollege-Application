from datetime import date
import json
from modules.login import *


def check_last_applied(database="database.json"):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()
    a = "0"
    b = "0"
    c = "0"
    for user in data["users"]:
        if user["username"] == LOGGED_IN_USER["username"]:
            a, b, c = user["last_applied"].split()
    res = date.today() - date(int(c), int(a), int(b))
    if res.days >= 7:
        msg = """
---------------------
Remember – you're going to want to have a job when you graduate.
Make sure that you start to apply for jobs today!
---------------------"""
        print(msg)
        time.sleep(3)


# Get first and last name by username
def get_name_noti(username, database):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()
    name = ""
    for user in data["users"]:
        if user["username"] == username:
            name = user["first_name"] + " " + user["last_name"]
            return name


def check_new_reg(database="database.json"):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()
    for user in data["users"]:
        if "username" not in LOGGED_IN_USER:
                continue
        if user["username"] == LOGGED_IN_USER["username"]:
            for usrn in user["new_reg"]:
                print(get_name_noti(usrn, database) + " has joined InCollege!")
                user["new_reg"].pop(0)
    with open(database, 'w+') as db:
        json.dump(data, db)
        db.close()


def buf_delete_job(deleted_job, database="database.json"):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()
    for user in data["users"]:
        for jobs in user["applied_jobs"]:
            if jobs == deleted_job["job_id"]:
                user["job_del"].append(deleted_job["title"])
                user["applied_jobs"].remove(deleted_job["job_id"])
    with open(database, 'w+') as db:
        json.dump(data, db)
        db.close()


def check_delete_job(database="database.json"):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()
    for user in data["users"]:
        if "username" not in LOGGED_IN_USER:
                continue
        if user["username"] == LOGGED_IN_USER["username"]:
            for jobs in user["job_del"]:
                print("\n\n---------------------")
                print("A job that you applied for has been deleted: " + jobs)
                print("---------------------")
                user["job_del"].remove(jobs)
    with open(database, 'w+') as db:
        json.dump(data, db)
        db.close()
