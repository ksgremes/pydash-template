"""
Dashboard - Helper functions

Helper functions used across the app
"""

import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def filter_df(df, filters={}, date_filters={}, variavel="tch"):
    # Filters data.frame
    CV = "CV_" + variavel.upper()
    MEDIA = "MEDIA_" + variavel.upper()
    COLDATA = "ATIVIDADE_" + variavel.upper()
    SAFRA = "SAFRA_" + variavel.upper()
    for col in date_filters.keys():
        df[COLDATA] = pd.to_datetime(df[COLDATA], format="%Y-%m-%d")
    if not bool(filters):
        return(df)
    selected = []
    for key, values in filters.items():
        selected.append(df[key].isin(values))
    selected = pd.concat(selected, axis=1)
    if bool(date_filters):
        selected_date = []
        for key, date_range in date_filters.items():
            date_range = pd.to_datetime(date_range)
            selected_date.append(df[COLDATA].between(date_range[0],
                                                     date_range[1],
                                                     inclusive=True))
        selected_date = pd.concat(selected_date, axis=1)
        selected = pd.concat([selected, selected_date], axis=1)
    selected = pd.concat([selected], axis=1)
    filtered_df = df.loc[selected.all(axis=1)]
    columns = ["SEQUENCIA", "NOME_LOCAL", "CONJUNTO", "ESTAGIO_CORTE",
               "ANO_PLANTIO", "MODELO", "AMBIENTE", "FASE", "CICLO", "HUB",
               SAFRA, COLDATA, CV, MEDIA]
    columns_dict = {
        "SEQUENCIA": "SEQUENCIA",
        "NOME_LOCAL": "NOME_LOCAL",
        "CONJUNTO": "CONJUNTO",
        "ESTAGIO_CORTE": "ESTAGIO_CORTE",
        "ANO_PLANTIO": "ANO_PLANTIO",
        "MODELO": "MODELO",
        "AMBIENTE": "AMBIENTE",
        "FASE": "FASE",
        "CICLO": "CICLO",
        "HUB": "HUB",
        SAFRA: "SAFRA",
        COLDATA: "DATA_ATIVIDADE",
        CV: "CV",
        MEDIA: "MEDIA"
    }
    return(filtered_df[columns].rename(columns=columns_dict))

def create_card(df, function, ftype, width=True, title="", colorCol=None):
    if ftype == "dynamic_plot":
        obj = dcc.Graph(figure=function(df, colorCol))
    elif ftype == "data_table":
        obj = html.Div([function(df, colorCol)],
                       style={"margin": "10px"})
    elif ftype == "fixed_plot":
        obj = function(df, colorCol)
    card = dbc.Col(
        html.Div(
            [
                html.H4(title),
                html.Hr(),
                obj
            ],
            style={
                "backgroundColor": "#ffffff",
                # "padding": "5px",
                "marginTop": "5px",
                "marginBottom": "5px",
                "borderRadius": "5px",
                "textAlign": "center",
                "height": "350px"
            }
        ),
        align="middle",
        width=width,
    )
    return(card)
