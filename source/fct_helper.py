"""
Dashboard - Helper functions

Helper functions used across the app
"""

import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def filter_df(df, filters={}, date_filters={}):
    # Filters data.frame
    # Don't edit this function
    for col in date_filters.keys():
        df[col] = pd.to_datetime(df[col])
    if not bool(filters):
        return(df)
    selected = []
    for key, values in filters.items():
        selected.append(df[key].isin(values))
    selected = pd.concat(selected, axis=1)
    selected_date = []
    for key, date_range in date_filters.items():
        selected_date.append(df[key].between(date_range["start"],
                                             date_range["end"],
                                             inclusive=True))
    selected_date = pd.concat(selected_date, axis=1)
    selected = pd.concat([selected, selected_date], axis=1)
    filtered_df = df.loc[selected.all(axis=1)]
    return(filtered_df)


def create_card(df, function, ftype, width=True, title="",
                filters={}, colorCol=None, date_filters={}):
    if ftype == "dynamic_plot":
        obj = dcc.Graph(figure=function(df, filters, colorCol, date_filters))
    elif ftype == "data_table":
        obj = function(df, filters, colorCol, date_filters)
    elif ftype == "fixed_plot":
        obj = function(df, filters, colorCol, date_filters)
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
                "margin": "5px",
                "borderRadius": "5px",
                "textAlign": "center"
            }
        ),
        align="middle",
        width=width,
    )
    return(card)
