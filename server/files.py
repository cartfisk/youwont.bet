import os
import shutil
import zipfile
import io

from server.constants import (
    AUDIO_ARCHIVE_PATH,
)


def delete_directory_contents(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)


def copy_directory(source, target):
    source_files = os.listdir(source)
    for file in source_files:
        file_path = os.path.join(source, file)
        shutil.copy(file_path, target)


def zip_directory_contents(source):
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode="w") as z:
        for file in os.listdir(source):
            z.write(os.path.join(source, file))
    data.seek(0)
    try:
        os.remove(AUDIO_ARCHIVE_PATH)
    except FileNotFoundError:
        print("No archive to delete.")
    archive = open(AUDIO_ARCHIVE_PATH, "wb")
    archive.write(data.read())
    archive.close()
