from modules.jobs2 import *
# 2 Ayman

def getAllJobs(database="database.json"):
    # load the database
    data = load_db(database)
    all_jobs = []
    # Add all the jobs in database to an array
    for user in data["users"]:
        for job in user["posted_jobs"]:
            all_jobs.append(job)
    return all_jobs

def writeAppliedJobs(database="database.json"):
    allJobs = getAllJobs(database)
    data = load_db(database)

    # Clear file if already exists
    f = open("MyCollege_appliedJobs.txt", "w")
    f.close()

    f = open("MyCollege_appliedJobs.txt", "a")
    printName = 0

    for job in allJobs:
        f.write(job["title"] + ":\n")
        for user in data["users"]:
            printName = 0
            if len(user["applied_jobs"]) >= 1: # If they have at least one applied job 
                for jobID in user["applied_jobs"]:
                        if jobID["job"] == job["job_id"]:
                            if printName == 0:
                                f.write("\t" + user["username"] + ": ")
                                printName = 1
                            f.write(jobID["user_description"] + "\n")
        f.write("==========\n")
    f.close()
