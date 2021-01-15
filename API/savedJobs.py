from modules.jobs2 import *
# 1 Ayman

def getAllJobs(database="database.json"):
    # load the database
    data = load_db(database)
    all_jobs = []
    # Add all the jobs in database to an array
    for user in data["users"]:
        for job in user["posted_jobs"]:
            all_jobs.append(job)
    return all_jobs

def writeSavedJobs(database="database.json"):
    allJobs = getAllJobs(database)
    data = load_db(database)

    # Clear file if already exists
    f = open("MyCollege_savedJobs.txt", "w")
    f.close()

    f = open("MyCollege_savedJobs.txt", "a")

    for user in data["users"]:
        if len(user["saved_jobs"]) >= 1: # If they have at least one saved job 
            f.write(user["username"] + ": ")
            for jobID in user["saved_jobs"]: # saved_jobs only stores IDs
                for job in allJobs: # Search all jobs to match jobID to job title
                    if jobID == user["saved_jobs"][-1] and jobID == job["job_id"]: # Last Job, dont add comma to end
                        f.write(job["title"])
                    elif jobID == job["job_id"]:
                        f.write(job["title"] + ",\t")
            f.write("\n==========\n")
    f.close()
