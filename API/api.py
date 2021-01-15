# This file is used for the api of the application.
# date started:11/15
# date ended:
# I had to modify chapt
import os

from modules.login import *
import json
import time
import random
import string
from modules.register import *
from modules.jobs2 import *
from modules.jobs import *


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


from modules.login import *
from modules.register import *


def api_account(database="database.json"):
    try:
        with open('../studentAccounts.txt') as f:
            data2 = f.read().splitlines()
    except IOError:
        print("studentAccounts.txt does not exist")
        return False

    for i in range(0, len(data2), 3):
        user_name = data2[i]
        passw = data2[i + 1]
        first = get_random_string(i + 2)
        last = get_random_string(i + 2)
        with open(database) as db:
            data = json.load(db)
            if len(data["users"]) >= 10:
                print("All permitted accounts have been created, please come back later")
                db.close()
                return False
        print(user_name, passw, first, last)
        limit = verify_register(user_name, passw, first, last, False)


#
# with open(file2,"r") as

# def jobs_api(file2,datab)
#  with open(file2,"r") as f:
#     data2=f.read().splitlines()

#    for i in range(0,len(data2))
#        title=data2[i]
#       passw=data2[i+1]


# post_job(title, description, employer, location, salary, database):

def getAllJobs(database="database.json"):
    # load the database
    data = load_db(database)
    all_jobs = []
    # Add all the jobs in database to an array
    for user in data["users"]:
        for job in user["posted_jobs"]:
            all_jobs.append(job)
    return all_jobs


def api_writeJobs(database="database.json"):
    allJobs = getAllJobs(database)
    data = load_db(database)

    # Clear file if already exists
    f = open("MyCollege_jobs.txt", "w")
    f.close()

    f = open("MyCollege_jobs.txt", "a")

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


def api_newJobs(database='database.json'):
    try:
        with open('newJobs.txt') as f:
            data = f.read().splitlines()
    except IOError:
        print("File newJobs.txt does not exist")
        return False
    # login('newUser46','tahirMon@1')
    login('Obama', '#Obama69')
    while (True):
        if not data:
            break
        else:
            #  print(data)
            title = data[0]
            desc = data[1]
            for i in range(len(data)):
                if data[i] == "&&&":
                    limit = i
                    break
            for i in range(2, limit):
                desc += data[i]
            emp = data[limit + 1]
            city = data[limit + 2]
            sal = data[limit + 3]
            del data[0:limit + 5]
            x = post_job(title, desc, emp, city, sal, database)


def api_training(database='database.json'):
    try:
        with open('newtraining.txt') as f:
            data = f.read().splitlines()
    except IOError:
        print("newtraining.txt does not exist")
        return False

    return data
