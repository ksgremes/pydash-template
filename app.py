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


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#202020",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
TOP_STYLE = {
    "position": "fixed",
    "top": "1rem",
    "left": "2rem",
    "margin-left": "16rem",
    "right": "2rem",
    "borderRadius": "5rem",
    "textAlign": "center",
}

sidebar = html.Div(
    [
        html.Div(
            [html.Img(src="assets/favicon.ico")],
            style={"textAlign": "center"}
        ),
        html.Hr(style={"borderTop": "2px solid #2196F3"}),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

with open("assets/columns.json", "r") as file:
    columns = json.load(file)["columns"]

topbar = html.Div(
    [
        html.H4(
            "Clique aqui para abrir os filtros",
            id="BOTAOFILTROS", n_clicks=0,
            style={
                "padding": "10px",
                "color": "#202020",
                "backgroundColor": "#2196F3",
                "borderRadius": "5px",
            }
        ),
        html.Div(id="DIVFILTROS")
    ],
    style=TOP_STYLE
)


content = html.Div(id="pageContent")

app.layout = html.Div([dcc.Location(id="url"), sidebar, topbar, content])


@app.callback(Output("pageContent", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    return(pages.render_page(pathname))


@app.callback([Output("DIVFILTROS", "children"),
               Output("pageContent", "style"),
               Output("BOTAOFILTROS", "children")],
              [Input("BOTAOFILTROS", "n_clicks")])
def mostra_filtros(n_clicks):
    if n_clicks % 2 == 0:
        # Esconder a div
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "margin-top": "3rem",
            "padding": "2rem 1rem"
        }
        return([], CONTENT_STYLE, "Clique aqui para abrir os filtros")
    else:
        return(filters.render_top(columns), {"display": "none"},
               "Fechar os filtros e atualizar a página")


if __name__ == "__main__":
    app.run_server(debug=True)
