from flask import Flask
from lockfile import LockFile
from definitions import ROOT_DIR
import os

step1_file_path = os.path.join(ROOT_DIR, "counter", "step1.txt")
if not os.path.exists(step1_file_path):
    with open(step1_file_path, 'w') as fp:
        pass

def counter1():

    lock = LockFile(step1_file_path)
    with lock:
        with open(step1_file_path, "r+") as f:
            fileContent = f.read()

            if fileContent == "":
                count = 1
            else:
                count = int(fileContent) + 1

            f.seek(0)
            f.write(str(count))
            f.truncate()

            return str(count)

