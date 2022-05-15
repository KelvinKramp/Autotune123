from datetime import datetime as dt
import os


# GET MODIFICATION DATE
def modification_date(filename):
    t = os.path.getmtime(filename)
    return dt.fromtimestamp(t)


# GET CURRENT TIME
def currentTimeUTC():
    return dt.now().strftime('%d/%m/%Y %H:%M:%S')


# CONVERT DATETIME INTO INTEGER TO EASE PARSING
def to_integer(dt_time):
    return 10000000000 * dt_time.year + 100000000 * dt_time.month + 1000000 * dt_time.day + 10000 * dt_time.hour + 100 * dt_time.minute + dt_time.second


# FILTER DATAFRAME FOR TODAY DATE
def filter_df_on_date(input_df, date):
    today_date = to_integer(date)
    today_date_numeric = str(today_date)[0:8]  # length of string = 9
    # print("TEST3")
    # print(input_df.columns)
    input_df['string_number_date'] = input_df['numeric_date'].apply(str)
    input_df = input_df[input_df['string_number_date'].str.contains(today_date_numeric)]
    input_df = input_df.reset_index(drop=True)
    input_df.drop(['string_number_date'],inplace=True,axis=1)
    return input_df
