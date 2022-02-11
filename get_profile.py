#!/usr/bin/env python
"""
Simplified version of the autotune python file created by viq
https://medium.com/@vicviq/how-to-run-autotune-when-not-using-openaps-82583df9bde

Things were inspired by https://github.com/MarkMpn/AutotuneWeb/
"""

from __future__ import absolute_import, with_statement, print_function, unicode_literals
from datetime import datetime
import json
import os.path
import logging
import sys
import requests
from ROOT_DIR import ROOT_DIR, checkdir
from correct_current_basals import correct_current_basals

PROFILE_FILES = ['autotune.json', 'profile.json', 'pumpprofile.json']
TIMED_ENTRIES = ['carbratio', 'sens', 'basal', 'target_low', 'target_high']


def get_current_profile(nightscout, token=None):
    """
    Try to get the active profile
    """
    # GET ACTIVE PROFILE BASED ON LATEST CREATION DATE
    # older version of get_profile used to rely on the resulting profile of the latest switch
    # the code beneath gave me a somewhat more consistent result
    r_url = nightscout + "/api/v1/profile.json"
    if token is not None:
        r_url = r_url + "?" + token
    p_list = requests.get(r_url).json()
    list_of_dates = [i["startDate"] for i in p_list]
    date_of_latest_activated_profile = max(list_of_dates)
    l = [i for i in p_list if (i["startDate"] == date_of_latest_activated_profile)][0]
    defaultprofile = l["defaultProfile"]
    profile = l["store"][defaultprofile]
    return profile


def normalize_entry(entry):
    """
    Clean up an entry before further processing
    """
    try:
        if entry["timeAsSeconds"]:
            pass
    except KeyError:
        entry_time = datetime.strptime(entry["time"], "%H:%M")
        entry[
            "timeAsSeconds"] = 3600 * entry_time.hour + 60 * entry_time.minute
    try:
        if entry["time"]:
            pass
    except KeyError:
        entry_hour = int(entry['timeAsSeconds'] / 3600)
        entry_minute = int(entry['timeAsSeconds'] % 60)
        entry["time"] = str(entry_hour).rjust(
            2, '0') + ":" + str(entry_minute).rjust(2, '0')

    entry["start"] = entry["time"] + ":00"
    entry["minutes"] = int(entry["timeAsSeconds"]) / 60
    return entry


def ns_to_oaps(ns_profile):
    """
    Convert nightscout profile to OpenAPS format
    """
    # CREATE EMPTY DICT
    oaps_profile = {}


    # ADD EXTRA PARAMETERS TO DICT
    oaps_profile["min_5m_carbimpact"] = 8.0
    oaps_profile["autosens_min"] = 0.7
    oaps_profile["autosens_max"] = 1.2
    oaps_profile["dia"] = float(ns_profile["dia"])
    oaps_profile["timezone"] = ns_profile["timezone"]


    # CREATE A LIST OF DICTS WITH BASAL PROFILES
    oaps_profile["basalprofile"] = []
    for entry_type in TIMED_ENTRIES:
        for entry in ns_profile[entry_type]:
            normalize_entry(entry)
    for basal_item in ns_profile["basal"]:
        oaps_profile["basalprofile"].append({
            "i":
            len(oaps_profile["basalprofile"]),
            "minutes":
            basal_item["minutes"],
            "start":
            basal_item["start"],
            "rate":
            float(basal_item["value"]),
        })


    # CREATE A DICT OF DICTS WITH TARGET LEVELS
    oaps_profile["bg_targets"] = {
        "units": ns_profile["units"],
        "user_preferred_units": ns_profile["units"],
        "targets": [],
    }
    targets = {}
    for low in ns_profile["target_low"]:
        low = normalize_entry(low)
        targets.setdefault(low["time"], {})
        targets[low["time"]]["low"] = {
            "i": len(targets),
            "start": low["start"],
            "offset": float(low["timeAsSeconds"]),
            "low": float(low["value"]),
        }
    for high in ns_profile["target_high"]:
        high = normalize_entry(high)
        targets.setdefault(high["time"], {})
        targets[high["time"]]["high"] = {"high": float(high["value"])}
    for time in sorted(targets.keys()):
        oaps_profile["bg_targets"]["targets"].append({
            "i":
            len(oaps_profile["bg_targets"]["targets"]),
            "start":
            targets[time]["low"]["start"],
            "offset":
            targets[time]["low"]["offset"],
            "low":
            targets[time]["low"]["low"],
            "min_bg":
            targets[time]["low"]["low"],
            "high":
            targets[time]["high"]["high"],
            "max_bg":
            targets[time]["high"]["high"],
        })


    # CREATE A DICT OF DICTS WITH INSULINE SENSITIVITY PROFILE
    oaps_profile["isfProfile"] = {"first": 1, "sensitivities": []}
    isf_p = {}
    for sens in ns_profile["sens"]:
        sens = normalize_entry(sens)
        isf_p.setdefault(sens["time"], {})
        isf_p[sens["time"]] = {
            "sensitivity": float(sens["value"]),
            "start": sens["start"],
            "offset": sens["minutes"],
        }
    for time in sorted(isf_p.keys()):
        if not isf_p[time]["sensitivity"] > 10: # TODO change into non-hardcoded code
            isf_p[time]["sensitivity"] = isf_p[time]["sensitivity"] * 18
        oaps_profile["isfProfile"]["sensitivities"].append({
            "i":
            len(oaps_profile["isfProfile"]["sensitivities"]),
            "sensitivity":
            isf_p[time]["sensitivity"],
            "offset":
            isf_p[time]["offset"],
            "start":
            isf_p[time]["start"],
        })


    # CREATE A DICT OF DICTS FOR CARB RATIO
    oaps_profile["carb_ratios"] = {
        "first": 1,
        "units": "grams",
        "schedule": []
    }
    cr_p = {}
    for cr in ns_profile["carbratio"]:
        cr = normalize_entry(cr)
        cr_p.setdefault(cr["time"], {})
        cr_p[cr["time"]] = {
            "start": cr["start"],
            "offset": cr["minutes"],
            "ratio": float(cr["value"]),
        }
    for time in sorted(cr_p.keys()):
        oaps_profile["carb_ratios"]["schedule"].append({
            "i":
            len(oaps_profile["carb_ratios"]["schedule"]),
            "start":
            cr_p[time]["start"],
            "offset":
            cr_p[time]["offset"],
            "ratio":
            cr_p[time]["ratio"],
        })
    oaps_profile["carb_ratio"] = oaps_profile["carb_ratios"]["schedule"][0][
        "ratio"]


    # SORT THE PROFILE
    sorted_profile = {}
    for key in sorted(oaps_profile.keys()):
        sorted_profile[key] = oaps_profile[key]


    # RETURN OPENAPS PROFILE
    return sorted_profile


def get_profile(nightscout, directory="myopenaps/settings", token=None):
    """
    Write profile in OpenAPS format to a directory
    """
    directory = os.path.join(os.path.expanduser('~'),directory)
    if nightscout.endswith("/"):
        nightscout = nightscout[:-1]
    profile = ns_to_oaps(get_current_profile(nightscout, token))
    profile = correct_current_basals(profile)
    logging.debug("Checking for directory: %s", directory)
    checkdir(directory)
    for profile_file in PROFILE_FILES:
        with open(os.path.join(directory, profile_file), 'w') as f:
            f.write(json.dumps(profile, indent=4))
    return profile

if __name__ == "__main__":
    profile = get_profile("NS_host")
    from pprint import pprint
    pprint(profile)

