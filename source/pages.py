"""
Content pages for dashboard

This is the file that should be edited to create different dashboard 'pages'
Each page is a function, and it should return the html code for the page
"""

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dtl
import dash_html_components as html
import pandas as pd
from source import fct_plots


def render_sidebar():
    # Render left sidebar for the dashboard
    # Edit this function to configure sidebar
    return([
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("Page 1", href="/main_page", active="exact"),
        dbc.NavLink("Page 2", href="/page-2", active="exact")
    ])


def render_page(pathname):
    # Render content on pages
    # Edit this function to configure the dashboard
    # Append paths to "if" block below
    if pathname == "/":
        return home_page()
    elif pathname == "/main_page":
        return main_page()
    elif pathname == "/page-1":
        return main_page()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


def home_page():
    # Home page for the dashboard
    # Just an example
    df = pd.read_csv("data.csv")
    return([
        dtl.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            )
    ])


def main_page():
    df = pd.read_csv("data.csv")
    line_plot = fct_plots.simple_plot(df, filters={"AREA": "A"})
    gauge_plot = fct_plots.gauge_plot(df, filters={"AREA": "B"})
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
