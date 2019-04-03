import os, shutil

from server.constants import (
    TRACK_NAMES,
    AUDIO_EXTENSION,
    ORIGINAL_AUDIO_BASE_PATH,
    ORIGINAL_AUDIO_FILEPATHS,
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
