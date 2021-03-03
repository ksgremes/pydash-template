# pydash
#
# This is a template for generating dashboards using the python
# library dash
#
# Kae Gremes - 2021

import base64
import io

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from source import pages
from source import filters
from dash.dependencies import Input, Output, State, MATCH, ALL
import json
import pandas as pd


app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#202020",
}

TOP_STYLE = {
    "position": "fixed",
    "top": "1rem",
    "left": "2rem",
    "marginLeft": "16rem",
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
            pages.render_sidebar(),
            vertical=True,
            pills=True,
        ),
        html.Hr(style={"borderTop": "2px solid #2196F3"}),
        html.H6("Filtros", style={"color": "#2196F3"}),
        html.Div(
            [
                html.H6(
                    "Clique aqui para abrir os filtros",
                    id="UIfilters", n_clicks=0,
                    style={
                        "padding": "10px",
                        "color": "#202020",
                        "backgroundColor": "#2196F3",
                        "borderRadius": "5px",
                    }
                )
            ]
        ),
        html.Hr(style={"borderTop": "2px solid #2196F3"}),

        html.H6("Upload de dados:", style={"color": "#2196F3"}),
        dcc.Upload(
            id='dataUpload',
            children=html.Div([
                'Arraste ou  ',
                html.A('Selecione um arquivo')
            ]),
            style={
                'width': '100%',
                'height': '40px',
                'lineHeight': '40px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'color': '#2196F3'
            }
        )
    ],
    style=SIDEBAR_STYLE,
)

with open("assets/columns.json", "r") as file:
    columns = json.load(file)["columns"]

topbar = html.Div(
    [
        html.Div(
            [filters.render_top(columns)],
            id="DIVfilters",
            style={"display": "none"}
        )
    ],
    style=TOP_STYLE
)


content = html.Div(id="DIVpageContent")

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    topbar,
    content,
    html.Div(id="DIVescondido", style={"display": "none"})
])

@app.callback(Output("DIVescondido", "children"),
              Input("dataUpload", "contents"))
def parse_contents(contents):
    if not contents:
        return(-1)
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')),
            sep=";", decimal=","
        )
    except Exception as e:
        print(e)
        return(-1)
    df.to_csv("data.csv")
    return(0)


@app.callback(Output("DIVpageContent", "children"),
              [Input("url", "pathname"),
               Input({"type": "SELECTfilter", "index": ALL}, "value"),
               Input("SELECTcolor", "value"),
               Input({"type": "SELECTdate", "index": ALL}, "start_date"),
               Input({"type": "SELECTdate", "index": ALL}, "end_date")])
def render_page_content(pathname, filters, colorCol, dates_start, dates_end):
    keys = [
        col["colName"] for col in columns
        if col["filterable"] == 1 and (col["type"] == "character" or
                                       col["type"] == "integer")
    ]
    date_columns = [
        col["colName"] for col in columns
            if col["filterable"] == 1 and col["type"] == "date"
    ]
    date_ranges = [{"start": dates_start[i], "end": dates_end[i]}
                        for i in range(len(dates_start))]
    return(pages.render_page(pathname,
                             dict(zip(keys, filters)),
                             colorCol,
                             dict(zip(date_columns, date_ranges))
    ))


@app.callback([Output("DIVfilters", "style"),
               Output("DIVpageContent", "style"),
               Output("UIfilters", "children")],
              [Input("UIfilters", "n_clicks")])
def mostra_filtros(n_clicks):
    if n_clicks % 2 == 0:
        # Esconder a div
        CONTENT_STYLE = {
            "marginLeft": "18rem",
            "marginRight": "2rem",
            "marginTop": "1rem"
        }
        return({"display": "none"}, CONTENT_STYLE, "Abrir filtros")
    else:
        return({"display": "block"}, {"display": "none"},
               "Fechar filtros")


if __name__ == "__main__":
    app.run_server(debug=True)
