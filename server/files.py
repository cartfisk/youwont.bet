import os
import shutil
import zipfile
import io

def delete_directory_contents(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)


def copy_directory(source, target):
    try:
        os.mkdir(target)
    except FileExistsError:
        print("directory: {} already exists".format(target))
    except FileNotFoundError:
        split_path = target.split("/")
        for i in range(len(split_path)):
            if i + 1 < len(split_path):
                try:
                    os.mkdir(os.path.join(*split_path[0:i + 1]))
                except FileExistsError:
                    print("directory: {} already exists".format(target))
    finally:
        try:
            os.mkdir(target)
        except FileExistsError:
            print("directory: {} already exists".format(target))

    source_files = os.listdir(source)
    for file in source_files:
        file_path = os.path.join(source, file)
        shutil.copy(file_path, target)


def zip_directory_contents(source, dest):
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode="w") as z:
        for file in os.listdir(source):
            z.write(os.path.join(source, file), file)
    data.seek(0)
    try:
        os.remove(dest)
    except FileNotFoundError:
        print("No archive to delete.")
    archive = open(dest, "wb")
    archive.write(data.read())
    archive.close()
