from server.files import delete_directory_contents
import os
import shutil
from pymongo import MongoClient


def reset_submissions():
    mongo = MongoClient(os.environ["DB"])
    submissions = mongo["youwont"]["submissions"]
    submissions.delete_many({})
    delete_directory_contents("assets/images/composite/iterations")
    delete_directory_contents("assets/images/submissions/accepted")
    delete_directory_contents("assets/images/submissions/pending")
    delete_directory_contents("assets/images/submissions/rejected")
    shutil.copy(
        "assets/images/composite/original/master.png",
        "assets/images/composite/master.png",
    )
    shutil.copy(
        "assets/images/composite/original/master.png",
        "static/master.png",
    )
