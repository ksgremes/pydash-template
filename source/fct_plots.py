"""
Dashboard plots
You should put the functions that generate plots here
It's important that these functions handle the filtering of the plots

Each function created here should have the following parameters:
    df (data.frame)
    filters (dict)
    colorCol (str)
    date_filters (dict)
"""

# import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import dash_daq as daq
import dash_table as dtl
from source import fct_helper as helper


def simple_plot(df, filters={}, colorCol=None, date_filters={}):
    # Creates a simple line chart along the dates
    # filters should be a dictionary

    filtered_df = helper.filter_df(df, filters, date_filters)
    if not colorCol:
        summary_df = filtered_df.groupby(["DATA"])
    else:
        summary_df = filtered_df.groupby(["DATA", colorCol])
    dates = []
    colors = []
    contaminacao = []
    for key, values in summary_df:
        if not colorCol:
            dates.append(key)
        else:
            dates.append(key[0])
            colors.append(key[1])
        contaminacao.append(sum(values.CONTAMINACAO) / sum(values.PRODUCAO))

    if not colorCol:
        summary_df = pd.DataFrame({
            "DATA": dates,
            "CONTAMINADO": contaminacao
        })
    else:
        summary_df = pd.DataFrame({
            "DATA": dates,
            colorCol: colors,
            "CONTAMINADO": contaminacao
        })
    if not colorCol:
        return(px.line(summary_df, x="DATA", y="CONTAMINADO", title='Titulo'))
    else:
        return(px.line(
            summary_df,
            x="DATA",
            y="CONTAMINADO",
            color=colorCol,
            title="Titulo (agora com cores!)"
        ))


def gauge_plot(df, filters={}, colorCol=None, date_filters={}):
    # Simple gauge plot
    filtered_df = helper.filter_df(df, filters, date_filters)
    perc = sum(filtered_df.CONTAMINACAO) / sum(filtered_df.PRODUCAO)*100
    return(daq.Gauge(
        id="gaugeplot",
        color={"gradient":False,
               "ranges":{"green":[0,.8],"yellow":[.8,.9],"red":[.9,1]}},
        showCurrentValue=True,
        value=perc,
        units="%",
        min=0,
        max=100,
        style={"verticalAlign": "middle"}
    ))


def create_table(df, filters={}, colorCol=None, date_filters={}):
    # Create datatable object
    filtered_df = helper.filter_df(df, filters, date_filters)
    return(dtl.DataTable(
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        data=filtered_df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'}
    ))
