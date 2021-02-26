"""
Dashboard plots
You should put the functions that generate plots here
It's important that these functions handle the filtering of the plots
"""

# import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import dash_daq as daq


def filter_df(df, filters={}):
    # Filters data.frame
    # Don't edit this function
    if not bool(filters):
        return(df)
    filtered_df = df.loc[(df[list(filters)] == pd.Series(filters)).all(axis=1)]
    return(filtered_df)


def simple_plot(df, filters={}):
    # Creates a simple line chart along the dates
    # filters should be a dictionary
    filtered_df = filter_df(df, filters)
    summary_df = filtered_df.groupby("DATA")
    dates = []
    contaminacao = []
    for date, values in summary_df:
        dates.append(date)
        contaminacao.append(sum(values.CONTAMINACAO) / sum(values.PRODUCAO))
    summary_df = pd.DataFrame({
        "DATA": dates,
        "CONTAMINADO": contaminacao
    })
    return(px.line(summary_df, x="DATA", y="CONTAMINADO", title='Titulo'))


def gauge_plot(df, filters={}):
    # Simple gauge plot
    filtered_df = filter_df(df, filters)
    perc = sum(filtered_df.CONTAMINACAO) / sum(filtered_df.PRODUCAO)*100
    return(daq.Gauge(
        id="gaugeplot",
        showCurrentValue=True,
        value=perc,
        units="%",
        min=0,
        max=100
    ))
