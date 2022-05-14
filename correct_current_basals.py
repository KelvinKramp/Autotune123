from datetime import timedelta
from dateutil import parser
import copy
from pprint import pprint
import os

name_intermediary_txt = "corrected_basal.txt"

# Correct profile if not a
def correct_current_basals(profile):
    with open(name_intermediary_txt, 'w') as f:
        _ = ""
    l = profile["basalprofile"]
    new_basals = []
    for i,j in enumerate(l):
        # if index of basal value is smaller than length -1 of total list
        if i < (len(l)-1):
            with open(name_intermediary_txt, 'a') as f:
                print(j, file=f)
            new_basals.append(j)
            # calculate difference in minutes current basal value with basal value of index-current+1
            d_compare2 = l[i+1]
            d_compare1 = l[i]
            diff = d_compare2["minutes"] - d_compare1["minutes"]
            # if difference >30 minutes
            if diff > 30:
                d_new = copy.deepcopy(d_compare1) # deepcopy to create independent object and prevent unwanted changes
                # mmodify d_new to format i, start (starttime), minutes (total minutes passed in day)
                for k in range((int(diff/30)-1)):
                    d_new["minutes"] = d_compare1["minutes"] +30*(k+1)
                    d_new["i"] = d_compare1["i"] + k+1
                    time = parser.parse(d_compare1['start'])
                    time_new = (time + timedelta(minutes=30*(k+1))).time()
                    d_new["start"] = time_new.strftime("%H:%M:%S")
                    with open(name_intermediary_txt, 'a') as f:
                        print(d_new, file=f)


        # last value of list
        if i == len(l)-1:
            with open(name_intermediary_txt, 'a') as f:
                print(j, file=f)

            # do the same thing as above but copare with the first value
            d_compare1 = l[0]
            d_compare2 = l[-1]
            diff = (parser.parse(d_compare1['start']) - parser.parse(d_compare2['start']))
            diff = (diff.seconds/60)
            if diff > 30:
                d_new2 = copy.deepcopy(d_compare2)
                for k in range((int(diff/30)-1)):
                    d_new2["minutes"] = d_compare2["minutes"]+30*(k+1)
                    d_new2["i"] = d_compare2["i"] + k+1
                    time = parser.parse(d_compare2['start'])
                    time_new = (time + timedelta(minutes=30*(k+1))).time()
                    d_new2["start"] = time_new.strftime("%H:%M:%S")
                    with open(name_intermediary_txt, 'a') as f:
                        print(d_new2, file=f)

    # read basals from text file into list
    basals=[]
    with open(name_intermediary_txt) as f:
        lines = f.readlines()
    for i,j in enumerate(lines):
        j = eval(j)
        j["i"] = i
        basals.append(j)
    profile["basalprofile"] = basals
    os.remove(name_intermediary_txt)
    return profile

if __name__ == "__main__":
    from get_profile import get_profile
    profile = get_profile("NS_HOST")
    print("PROFILE1")
    pprint(profile)
    profile2= correct_current_basals(profile)
    print("PROFILE2")
    pprint(profile)