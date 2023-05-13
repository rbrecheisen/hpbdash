import os
import json
import shutil
import pandas as pd
import matplotlib.pyplot as plt

from django.shortcuts import render, redirect
from django.views.static import serve
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from .models import QueryModel, QueryResultModel, ReportItemModel, ReportModel

from barbell2_castor import CastorQuery


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def get_queries(request):
    queries = QueryModel.objects.all()
    if not os.path.isfile(settings.CASTOR_DB_FILE):
        message = 'database: not found'
    else:
        message = f'database: {settings.CASTOR_DB_FILE}'
    if not os.path.isfile(settings.CASTOR_DD_FILE):
        message += ', data dictionary file: not found'
    else:
        message += f', data dictionary file: {settings.CASTOR_DD_FILE}'
    return render(request, 'queries.html', context={'queries': queries, 'message': message})


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def create_query(request):
    QueryModel.objects.create(sql_statement=request.POST.get('sql_statement'))
    return redirect('/queries/')


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def delete_query(request, query_id):
    query = QueryModel.objects.get(pk=query_id)
    query.delete()
    return redirect('/queries/')


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def execute_query(request, query_id):
    # check if SQL database is present. if not, return error page
    if not os.path.isfile(settings.CASTOR_DB_FILE) or os.path.getsize(settings.CASTOR_DB_FILE) == 0:
        errors = [f'Database file {settings.CASTOR_DB_FILE} not found or empty. Did Prefect pipeline run?']
        return render(request, 'errors.html', context={'errors': errors})    
    # run query and store results in csv file
    query_engine = CastorQuery(settings.CASTOR_DB_FILE)
    query = QueryModel.objects.get(pk=query_id)
    query_engine.execute(query.sql_statement)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    query_result_file = os.path.join(settings.CASTOR_QUERY_RESULT_DIR, f'query-{query_id}-result-{timestamp}.csv')
    query_result = QueryResultModel.objects.create(
        query=query,
        result_file=query_result_file,
    )
    query_engine.to_csv(query_result.result_file)
    # redirect to query result page
    return redirect(f'/queries/{query_id}/results/{query_result.id}/')
    
    
"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def get_result(request, query_id, result_id):
    query_result = QueryResultModel.objects.get(pk=result_id)
    # note: conversion to dataframe results integers in being converted to floats
    # use data dictionary to perform conversion
    df = query_result.as_df()
    return render(request, 'result.html', context={
        'query': query_result.query, 'query_result': query_result, 'nr_rows': len(df.index), 'columns': df.columns, 'data': df.to_numpy()})
    
    
"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def download_result(request, query_id, result_id):
    query_result = QueryResultModel.objects.get(pk=result_id)
    filepath = query_result.result_file
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


"""-------------------------------------------------------------------------------------------------------------------
"""
def get_reports(request):
    reports = ReportModel.objects.all()
    return render(request, 'reports.html', context={'reports': reports})


"""-------------------------------------------------------------------------------------------------------------------
"""
def create_report(request):
    report_name = request.POST.get('report_name', None)
    report = ReportModel.objects.create(report_name)
    # how do I get the queries checked for this report from the queries.html
    return redirect('/queries/')
