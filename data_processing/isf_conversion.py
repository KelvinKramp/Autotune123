import numpy as np
import pandas as pd

def isf_conversion(df):
    # https://stackoverflow.com/questions/24029659/python-pandas-replicate-rows-in-dataframe
    reps = [2 if val=="ISF[mg/dL/U]" else 1 for val in df.Parameter]
    df = df.loc[np.repeat(df.index.values, reps)]
    df = df.reset_index(drop=True)
    df["Pump"][1] = round(float(df["Pump"][1])/18, 2)
    df["Autotune"][1] = round(float(df["Autotune"][1])/18, 2)
    df["Parameter"][1] = "ISF[mmol/L/U]"
    return df

if __name__ == "__main__":
    from .get_recommendations import get_recommendations
    df = get_recommendations()
    df = isf_conversion(df)
    df["Pump"][3] = ""
    df["Pump"] = df["Pump"].replace('',np.nan).astype(float)
    df["Autotune"] = df["Autotune"].replace('',np.nan).astype(float)
    df["Autotune"] = df['Autotune'].apply(lambda x: f'{x:.2f}')
    df["Pump"] = df['Pump'].apply(lambda x: f'{x:.2f}')
    df = df.replace("nan", "")
    print(df)