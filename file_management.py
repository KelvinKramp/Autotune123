import os
from definitions import ROOT_DIR, PROFILE_FILES
from log import logging

def mv_files(files_list=None):
    if files_list is None:
        files_list = PROFILE_FILES
    for i in files_list:
        old_path = os.path.join(ROOT_DIR, i)
        new_path = os.path.join(ROOT_DIR, "myopenaps","settings",i)
        # print("Move:")
        # print(old_path)
        # print("To:")
        # print(new_path)
        os.replace(old_path, new_path)

def checkdir(dir):
    if not os.path.isdir(dir):
        logging.error("Directory not found")
        try:
            os.makedirs(dir)
        except Exception as e:
            logging.error("Error occured during opening directory:"+dir)
            logging.error(e)