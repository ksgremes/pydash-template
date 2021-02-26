# pydash
#
# This is a template for generating dashboards using the python
# library dash
#
# Kae Gremes - 2021

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from source import pages
from source import filters
from dash.dependencies import Input, Output
import json


app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
}

TOPBAR_STYLE = {
    "position": "fixed",
    "left": "16rem",
    "right": 0,
    "top": 0,
    "height": "6rem",
    "padding": "2rem 2rem",
    "backgroundColor": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginTop": "6rem",
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 2rem",
    "backgroundColor": "#000000"
}

sidebar = html.Div(
    [
        html.Div([
            html.Img(
                src="assets/favicon.ico",
                style={
                    "width": "30%"
                })
        ], style={"textAlign": "center"}),
        html.Hr(),
        dbc.Nav(
            pages.render_sidebar(),
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

with open("assets/columns.json", "r") as file:
    columns = json.load(file)["columns"]

topbar = html.Div(
    filters.render_top(columns),
    style=TOPBAR_STYLE
)

content = html.Div(id="pageContent", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, topbar, content])


@app.callback(Output("pageContent", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    return(pages.render_page(pathname))


if __name__ == "__main__":
    app.run_server(debug=True)
