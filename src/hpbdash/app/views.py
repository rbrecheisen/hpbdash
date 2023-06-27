import os
import json
import pandas as pd

from django.shortcuts import render, redirect
from django.views.static import serve
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required

from .models import QueryModel, QueryResultModel, ReportModel

from barbell2_castor import CastorQueryRunner


@login_required
def get_queries(request):
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


@login_required
def create_query(request):
    QueryModel.objects.create(name=request.POST.get('name'), sql=request.POST.get('sql'))
    return redirect('/queries/')


@login_required
def delete_query(request, query_id):
    query = QueryModel.objects.get(pk=query_id)
    query.delete()
    return redirect('/queries/')


@login_required
def execute_query(request, query_id):
    # get query
    query = QueryModel.objects.get(pk=query_id)
    # load JSON data Castor
    with open(settings.CASTOR_JSON_FILES['dpca'], 'r') as f:
        data = json.load(f)
    df_data = {}
    for field_name in data.keys():
        df_data[field_name] = data[field_name]['field_values']
    df = pd.DataFrame(data=df_data)
    for field_name in data.keys():
        if data[field_name]['field_type'] == 'date':
            df[field_name] = pd.to_datetime(df[field_name], dayfirst=True, errors='coerce')
    df2 = df.query(query.sql)
    print(df2)
    # redirect to query result page
    return redirect('/queries/')
    
    
"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def get_result(request, result_id):
    query_result = QueryResultModel.objects.get(pk=result_id)
    # note: conversion to dataframe results integers in being converted to floats
    # use data dictionary to perform conversion
    df = query_result.as_df()
    return render(request, 'result.html', context={
        'query': query_result.query, 'query_result': query_result, 'nr_rows': len(df.index), 'columns': df.columns, 'data': df.to_numpy()})


"""-------------------------------------------------------------------------------------------------------------------
"""
def delete_result(request, result_id):
    query_result = QueryResultModel.objects.get(pk=result_id)
    query_result.delete()
    return redirect('/queries/')
    
    
"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def download_result(request, result_id):
    query_result = QueryResultModel.objects.get(pk=result_id)
    filepath = query_result.result_file
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def delete_result(request, result_id):
    query_result = QueryResultModel.objects.get(pk=result_id)
    query_result.delete()
    return redirect('/queries/')


"""-------------------------------------------------------------------------------------------------------------------
"""
def get_reports(request):
    reports = ReportModel.objects.all()
    return render(request, 'reports.html', context={'reports': reports})


"""-------------------------------------------------------------------------------------------------------------------
"""
def create_report(request):
    # create report object
    end_date = request.POST.get('end_date')
    start_date = request.POST.get('start_date')
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    report = ReportModel.objects.create(name=f'report-{timestamp}', start_date=start_date, end_date=end_date)    
    # select queries
    queries = QueryModel.objects.all()
    selected_queries = []
    for query in queries:
        query_checkbox_id = f'{query.id}_cbx'
        if request.POST.get(query_checkbox_id, None) is not None:
            selected_queries.append(query)
    # update selected queries with BETWEEN dates info
    for query in selected_queries:
        sql_statement = query.sql
        if 'WHERE' in sql_statement:
            items = query.sql_statement.split('WHERE')
            select = items[0]
            where_clause = items[1]
            where_clause += f'WHERE {settings.CASTOR_DATOK_NAMES[query.database]} BETWEEN "{start_date}" AND "{end_date}" {where_clause}'
            sql_statement = select + where_clause
            if not sql_statement.endswith(';'):
                sql_statement += ';'
        else:
            if sql_statement.endswith(';'):
                sql_statement = sql_statement[:-1]
            sql_statement += f' WHERE {settings.CASTOR_DATOK_NAMES[query.database]} BETWEEN "{start_date}" AND "{end_date}";'
        # ReportItemModel.objects.create(report=report, sql_statement=sql_statement)
    return redirect('/reports/')


"""-------------------------------------------------------------------------------------------------------------------
"""
def delete_report(request, report_id):
    report = ReportModel.objects.get(pk=report_id)
    report.delete()
    return redirect('/reports/')
