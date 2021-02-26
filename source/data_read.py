# functions to read the data

import pandas as pd
import datetime as dta


def import_df(filepath):
    return(pd.read_csv(filepath))


def summary(column):
    if column.dtype == "int64":
        return("Int")
    else:
        return("NotInt")


if __name__ == "__main__":
    df = import_df("../data.csv")
    datas = [dta.datetime.strptime(mes, "%Y-%m-%dT%H:%M:%SZ")
             for mes in df.DATA]
    print(min(datas))
    print(max(datas))
    column = "COLUNA"
    print(min(df[column]))
