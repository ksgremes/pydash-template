# Creates the filters on top of the page


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json


def render_top(columns):
    width = "33%"
    box = html.Div(
        [
            html.H3("Seleção de dados:"),
            dbc.Nav(
                [create_filter(col, width)
                    for col in columns if col["filterable"] != 0
                    and col["quickbar"] != 1],
                vertical=False
                )
        ],

    )
    return(html.Div(
        [box],
        style={
            "backgroundColor": "#ffffff",
            "color": "#079400",
            "borderRadius": "5px",
            "textAlign": "left",
            "padding": "5px "
        }
    ))


def create_filter(column, width, quickbar=0):
    df = pd.read_csv("data.csv", sep=";", decimal=",")
    if column["type"] == "character" or column["type"] == "integer":
        values = df[column["colName"]].unique()
        values = [val for val in values if str(val) != "nan"]
        filt = dcc.Dropdown(
            id={"type": "SELECTfilter", "index": f"SELECT{column['colName']}"},
            options=[{"label": val, "value": val} for val in values],
            value=values,
            multi=True,
            clearable=True,
            style=({"color": "#000000"}
                   if quickbar == 1 else
                   {"color": "#000000", "height": "150px",
                    "overflowY": "scroll"})
        )
    elif column["type"] == "date":
        datas = pd.concat([df["ATIVIDADE_TCH"], df["ATIVIDADE_TPH"],
                           df["ATIVIDADE_PCC"]], axis=0)
        datas = pd.to_datetime(datas, format="%Y-%m-%d")
        datas = pd.date_range(start=min(datas),
                              end=max(datas) + pd.DateOffset(months=3),
                              freq="3M", normalize=False, closed="left")
        datas_num = pd.to_numeric(datas)
        datas = datas.strftime("%b-%Y")
        marks = {
            str(datas_num[i]):
            {"label": datas[i], "style": {"writingMode": "vertical-lr",
                                          "textOrientation": "sideways",
                                          "height": "100px"
            }}
            for i in range(len(datas))
        }
        filt = dcc.RangeSlider(
            id={"type": "SELECTdate", "index": f"SELECT{column['colName']}"},
            min=min(datas_num),
            max=max(datas_num),
            value=[min(datas_num),max(datas_num)],
            step=None,
            marks=marks
        )
    return(html.Div(
        [html.H6(f"Filtro: {column['colName']}"), filt],
        style={"width": width, "padding": "5px", "textAlign": "center"}
    ))


if __name__ == "__main__":
    with open("../assets/columns.json", "r") as file:
        columns = json.load(file)
    columns = columns["columns"]
    print(create_filter(columns[0]))
