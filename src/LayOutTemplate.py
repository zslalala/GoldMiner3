import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd


def GetTables(OperationDataFrame,TableId,HavingP=False,HtmlPId=None,ChildrenP=None):

    if HavingP == False:
        return GetOnlyTable(OperationDataFrame,TableId)

    if HavingP == True:
        return GetHtmlPAndTable(OperationDataFrame,TableId,HtmlPId,ChildrenP)

def GetOnlyTable(OperationDataFrame,TableId):

    table = html.Div(
        [dash_table.DataTable(
            id=TableId,
            columns=[{"name": i, "id": i} for i in OperationDataFrame.columns],
            data=OperationDataFrame.to_dict('records'),
        )]
    )

    return table


def GetHtmlPAndTable(OperationDataFrame,TableId,HtmlPId,ChildrenP):

    table = html.Div(
        [html.P(id=HtmlPId, children=ChildrenP),
         dash_table.DataTable(
             id=TableId,
             columns=[{"name": i, "id": i} for i in OperationDataFrame.columns],
             data=OperationDataFrame.to_dict('records'),
         )]
    )

    return table