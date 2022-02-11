import pandas as pd
import glob
import os
import datetime
import subprocess


recommendations_file_path = "myopenaps/autotune/autotune_recommendations.log"
recommendations_file = os.path.join(os.path.expanduser('~'), recommendations_file_path)


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def check_file_datetime():
    # check if file is older than 10 minutes ago, if so raise error
    creation_time = modification_date(recommendations_file)
    current_time = datetime.datetime.now()

    return True
    if (current_time.minute - 10) < creation_time.minute < (current_time.minute + 1):
        return True
    else:
        raise AssertionError(
            "Recommendations file old, evaluate and rerun autotune or increase comparison time treshold")


def get_recommendations():
    if check_file_datetime():
        command = "cp {} ./new_profile.csv".format(recommendations_file)
        subprocess.call(command, shell=True)
        df = pd.read_csv("./new_profile.csv",delimiter = "|",)
        command1 = "rm new_profile.csv"
        subprocess.call(command1, shell=True)
        df = df.drop([0])
        # remove spaces in column names
        df.columns = df.columns.str.replace(' ', '')
        # remove spaces within values of column
        for i in df.columns:
            df[i] = df[i].str.replace(' ', '')
        return df


if __name__ == "__main__":
    df = get_recommendations()
    print(df)
