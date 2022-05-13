import os
import sys


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def checkdir(dir):
    if not os.path.isdir(dir):
        print("Directory not found")
        try:
            os.makedirs(dir)
        except Exception as e:
            print("Error occured during opening directory")
            print(e)
            sys.exit(("Error occured during making of directory" + dir))