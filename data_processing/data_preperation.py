from .get_recommendations import get_recommendations
from .get_filtered_data import get_filtered_data
from .create_graph import create_graph
from .table_calculations import adjust_table
from .isf_conversion import isf_conversion, remove_isf_conversion
from .clean_values import clean_values
import pandas as pd

def data_preperation(dropdown_value, df=pd.DataFrame()):

    if df.empty:
        # convert Autotune recommendationns file into pd df
        df_recommendations = get_recommendations()
    else:
        df_recommendations = remove_isf_conversion(df)
    print("PANDAS DATAFRAME")
    print(df_recommendations)
    # get the lists x, y1 and y2 from the pd df based on dropdown value
    x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)

    # TODO: create a peak in the curve if wanted
    # print(type(y1))
    # print(type(y2))
    # print(len(x))
    # take 5 basal values with the 3th based on time input
    # increase middel value y2 with given percentage
    # increase surrounding y2 values with percentage/2 and percentage /4.

    # create graph from lists
    graph = create_graph(x, y1, y2)
    # replace the pump and autotune column with y1 and y2 from the start_row_index
    df_recommendations = adjust_table(df_recommendations, [y1, y2], ["Pump", "Autotune"],
                                      4)  # 4 is startrowindex for changing the df
    # convert isf to mmol/L
    df_recommendations = isf_conversion(df_recommendations)
    df_recommendations = clean_values(df_recommendations)
    # calculate totals
    y1_sum_graph = round((sum([x for x in y1 if str(x) != 'nan'])), 3)
    y2_sum_graph = round(sum([x for x in y2 if str(x) != 'nan']), 3)
    return df_recommendations, graph, y1_sum_graph, y2_sum_graph
