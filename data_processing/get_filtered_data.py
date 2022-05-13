import numpy as np
from scipy.signal import savgol_filter


def get_filtered_data(df, filter="No filter"):
    # clean lists by removing sensitivity, removing IC ratio, removing empty values and converting strings
    # with ratios to floats.

    # x
    l = df["Parameter"].to_list()
    l_time = []
    for string in l[3:]:
        if string == "":
            string = np.nan
            l_time.append(string)
        else:
            l_time.append(string)

    # y1
    l1 = df["Pump"].to_list()
    l1_new = []
    for string in l1[3:]:
        if string == "":
            string = np.nan
            l1_new.append(string)
        else:
            l1_new.append(string)
    l1 = list(map(float, l1_new))

    # y2
    l2 = df["Autotune"].to_list()
    l2 = l2[3:]
    l2_new = []
    for string in l2:
        if string == "":
            string = np.nan
            l2_new.append(string)
        else:
            l2_new.append(string)
    l2 = list(map(float, l2_new))
    l2 = np.asarray(l2)

    # apply filter
    l2_clean = l2[::2]  # remove empty values
    if filter == "No filter":
        l3 = l2_clean
    else:
        if filter == "Savitzky-Golay 11.6":
            l3 = savgol_filter(l2_clean, 11, 6)
        elif filter == "Savitzky-Golay 17.5":
            l3 = savgol_filter(l2_clean, 17, 5)
        elif filter == "Savitzky-Golay 23.3":
            l3 = savgol_filter(l2_clean, 23, 3)

    # update numpy array of recommendations (l2) with filtered values
    n = 0
    for i, j in enumerate(l2):
        if not np.isnan(j):
            l2[i] = l3[n]
            n += 1
    l2 = l2.tolist()

    # round numbers
    l2 = [round(num, 2) for num in l2]

    # use easy identifiable variable names
    x = l_time
    y1 = l1
    y2 = l2

    return x,y1,y2
