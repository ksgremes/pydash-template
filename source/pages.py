"""
Content pages for dashboard

This is the file that should be edited to create different dashboard 'pages'
Each page is a function, and it should return the html code for the page

Each page has to accept the arguments:
    filters, colorCol, date_filters (see examples below)
"""

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dtl
import dash_html_components as html
import pandas as pd
from source import fct_plots
from source import fct_helper as helper


def render_sidebar():
    # Render left sidebar for the dashboard
    # Edit this function to configure sidebar
    return([
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("Page 1", href="/main_page", active="exact"),
        dbc.NavLink("Page 2", href="/page-2", active="exact")
    ])


def render_page(pathname, filters={}, colorCol=None, date_filters={}):
    # Render content on pages
    # Edit this function to configure the dashboard
    # Append paths to "if" block below
    if pathname == "/":
        return home_page(filters, colorCol, date_filters)
    elif pathname == "/main_page":
        return main_page(filters, colorCol, date_filters)
    elif pathname == "/page-2":
        return test_page(filters, colorCol, date_filters)
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


def home_page(filters, colorCol, date_filters):
    # Home page for the dashboard
    # Just an example
    df = pd.read_csv("data.csv", sep=";", decimal=",")
    filtered_df = helper.filter_df(df, filters, date_filters)
    return([
        dtl.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in filtered_df.columns],
            data=filtered_df.to_dict('records'),
            )
    ])


def main_page(filters, colorCol, date_filters):
    df = pd.read_csv("data.csv", sep=";", decimal=",")
    line_plot = fct_plots.simple_plot(df, filters=filters,
                                      colorCol=colorCol,
                                      date_filters=date_filters)
    gauge_plot = fct_plots.gauge_plot(df, filters=filters,
                                      date_filters=date_filters)
    return([
        html.Div([
                html.Div(
                    dcc.Graph(figure=line_plot),
                    className="col-sm-8",
                ),
                html.Div(
                    gauge_plot,
                    className="col-sm-4",
                    style={"backgroundColor": "#888888"}
                )
            ],
            className="row"
        )
    ])


def test_page(filters, colorCol, date_filters):
    df = pd.read_csv("data.csv", sep=";", decimal=",")
    linha1 = dbc.Row(
        [
            helper.create_card(df, fct_plots.simple_plot,
                               title="Grafico qualquer", width=8,
                               ftype="dynamic_plot",
                               filters=filters, colorCol=colorCol,
                               date_filters=date_filters),
            helper.create_card(df, fct_plots.gauge_plot,
                               title="Velocimetro", width=4,
                               ftype="fixed_plot",
                               filters=filters, colorCol=colorCol,
                               date_filters=date_filters)
        ]
    )
    linha2 = dbc.Row(
        [
            helper.create_card(df, fct_plots.create_table,
                               title="Dados", width=12,
                               ftype="data_table",
                               filters=filters, colorCol=colorCol,
                               date_filters=date_filters)
        ]
    )
    return(
        dbc.Container(
            [
                linha1, linha2
            ],
            fluid=True
        )
    )
