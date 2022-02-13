import pandas as pd


def adjust_table(df, new_columns, column_names, start_row_index):
    """Insert the given columns (new_columns = list of new columns) into the pandas dataframe based on column names and start index"""
    for i,new_column in enumerate(new_columns):
        if new_column: # if column not emptuy
            # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html
            df.loc[start_row_index:len(df[column_names[i]]),column_names[i]] = new_column
    return df



if __name__ == "__main__":
    from get_recommendations import get_recommendations
    df = get_recommendations()
    l3 = ['0.868', '', '1.218', '', '1.180', '', '1.158', '', '1.114', '', '1.119', '', '0.469',
          '', '0.534', '', '0.541', '', '0.415', '', '0.381', '', '0.381', '', '0.425', '', '0.482', '', '0.600', '',
          '0.600', '', '0.600', '', '0.503', '', '0.480', '', '0.590', '', '0.594', '', '0.600', '', '0.545', '',
          '20000', '']
    new_columns = [[], l3]
    column_names = ["Pump", "Autotune"]
    start_row_index = 4
    adjust_table(df, new_columns, column_names, start_row_index)