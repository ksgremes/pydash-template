# Creates the filters on top of the page


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import datetime as dta
import pandas as pd
import json


def render_top(columns):
    num_cols = sum([col["filterable"] for col in columns])
    separador = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([html.H3("Cores nos gráficos:")],
                            style={
                                "textAlign": "right",
                                "padding": "5px"
                            },
                            width=5),
                    dbc.Col(
                        [dcc.Dropdown(
                            id="separador",
                            options=[{"label": col["colName"],
                                      "value": col["colName"]}
                                        for col in columns],
                                      placeholder="Selecione uma coluna",
                                      clearable=True
                        )],
                        style={
                            "textAlign": "left",
                            "color": "#000000",
                            "padding": "5px"
                        },
                        width=6
                    )

                ]
            ),
            html.Hr(style={"borderTop": "2px solid #2196F3"})
        ]
    )
    box = html.Div(
        [
            html.H3("Seleção de dados:"),
            dbc.Nav(
                [create_filter(col, num_cols)
                    for col in columns if col["filterable"] != 0],
                vertical=False
                )
        ],

    )
    return(html.Div(
        [separador, box],
        style={
            "backgroundColor": "#202020",
            "color": "#2196F3",
            "borderRadius": "5px",
            "textAlign": "left",
            "padding": "5px "
        }
    ))


def create_filter(column, num_cols):
    df = pd.read_csv("data.csv")
    # if column["type"] == "integer":
    #     filt = dcc.Slider(
    #         min=min(df[column["colName"]]),
    #         max=max(df[column["colName"]])
    #     )
    if column["type"] == "character" or column["type"] == "integer":
        values = df[column["colName"]].unique()
        filt = dcc.Dropdown(
            options=[{"label": val, "value": val} for val in values],
            value=values,
            multi=True,
            clearable=True,
            style={"height": "100px", "color": "#000000"}
        )
    elif column["type"] == "date":
        datas = [dta.datetime.strptime(mes, "%Y-%m-%dT%H:%M:%SZ")
                 for mes in df[column["colName"]]]
        filt = dcc.DatePickerRange(
            start_date=min(datas),
            end_date=max(datas),
            display_format="Y-M-D",
            style={"height": "100px"}
        )
    # return(html.Div(filt, style={"width": f"{95/num_cols:.2f}%", "padding": "5px"}))
    return(html.Div(
        [html.H6(column["colName"]), filt],
        style={"width": "33%", "padding": "5px", "textAlign": "center"}
    ))


if __name__ == "__main__":
    with open("../assets/columns.json", "r") as file:
        columns = json.load(file)
    columns = columns["columns"]
    print(create_filter(columns[0]))
