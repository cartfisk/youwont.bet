import os, shutil, zipfile, io, pathlib

from server.constants import (
    TRACK_NAMES,
    AUDIO_EXTENSION,
    AUDIO_BASE_PATH,
    AUDIO_FILEPATHS,
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
    with zipfile.ZipFile(data, mode='w') as z:
        for file in os.listdir(source):
            z.write(file)
    data.seek(0)
    shutil.remove(AUDIO_ARCHIVE_PATH)
    archive = open(AUDIO_ARCHIVE_PATH, "wb")
    archive.write(data)
    archive.close()
