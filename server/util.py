from server.files import delete_directory_contents, copy_directory
import os
import shutil
from pymongo import MongoClient
from datetime import datetime


def reset_submissions():
    mongo = MongoClient(os.environ["DB"])
    submissions = mongo["youwont"]["submissions"]
    submissions.delete_many({})

    now = str(datetime.now().timestamp()).replace(".", " ")

    copy_directory("assets/images/composite/iterations", "assets/images/backups/{}/composite/iterations".format(now))
    delete_directory_contents("assets/images/composite/iterations")

    copy_directory("assets/images/submissions/accepted", "assets/images/backups/{}/submissions/accepted".format(now))
    delete_directory_contents("assets/images/submissions/accepted")

    copy_directory("assets/images/submissions/pending", "assets/images/backups/{}/submissions/pending".format(now))
    delete_directory_contents("assets/images/submissions/pending")

    copy_directory("assets/images/submissions/rejected", "assets/images/backups/{}/submissions/rejected".format(now))
    delete_directory_contents("assets/images/submissions/rejected")

    shutil.copy(
        "assets/images/composite/original/master.png",
        "assets/images/composite/master.png",
    )
    shutil.copy(
        "assets/images/composite/original/master.png",
        "static/master.png",
    )
