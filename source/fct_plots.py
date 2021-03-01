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


def simple_plot(df, filters={}, colorCol=None, date_filters={}):
    # Creates a simple line chart along the dates
    # filters should be a dictionary

    filtered_df = filter_df(df, filters, date_filters)
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
    filtered_df = filter_df(df, filters, date_filters)
    perc = sum(filtered_df.CONTAMINACAO) / sum(filtered_df.PRODUCAO)*100
    return(daq.Gauge(
        id="gaugeplot",
        showCurrentValue=True,
        value=perc,
        units="%",
        min=0,
        max=100
    ))
