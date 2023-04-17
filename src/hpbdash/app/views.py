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

from .models import QueryModel, QueryResultModel

from barbell2_castor import CastorQuery


""" -------------------------------------------------------------------------------------------------------------------
"""
@login_required
def upload_data_dictionary(request):
    # get uploaded file path
    f = request.FILES.get('file')
    if isinstance(f, InMemoryUploadedFile):
        f_path = os.path.join(settings.MEDIA_ROOT, default_storage.save(f.name, ContentFile(f.read())))
    elif isinstance(f, TemporaryUploadedFile):
        f_path = shutil.copy(f.temporary_file_path, settings.MEDIA_ROOT)
    else:
        raise RuntimeError('could not determine path uploaded file')
    # read options
    options = {}
    df_options = pd.read_excel(f_path, sheet_name='Field options', dtype=str)
    for idx, row in df_options.iterrows():
        option_group = row['Option group name']
        if pd.notna(option_group):
            option = row['Option name']
            value = row['Option value']
            if option_group not in options.keys():
                options[option_group] = {}
            options[option_group][value] = option
    # read data dictionary and update with options
    dd = {}
    df_fields = pd.read_excel(f_path, sheet_name='Study variable list', dtype=str)
    for idx, row in df_fields.iterrows():
        variable_name = row['Variable name']
        field_type = row['Original field type']
        label = row['Field label']
        option_group = row['Optiongroup name']
        if variable_name not in dd.keys():
            dd[variable_name] = {
                'label': label,
                'field_type': field_type,
                'option_group': None,
            }
        if pd.notna(option_group):
            dd[variable_name]['option_group'] = options[option_group]
    # write data dictionary to file
    with open(settings.CASTOR_DD_FILE, 'w') as f:
        json.dump(dd, f, indent=4)
    # redirect to queries page
    return redirect('/queries/')


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def get_fields(request):
    # Load data dictionary settings.CASTOR_DD_FILE
    with open(settings.CASTOR_DD_FILE, 'r') as f:
        data = json.load(f)
    for field_name in data.keys():
        field = data[field_name]
        
    # Convert to table
    return render(request, 'fields.html', context={'columns': columns, 'data': data})


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def get_option_groups(request):
    # Load data dictionary settings.CASTOR_DD_FILE
    # Convert to table
    return render(request, 'option_groups.html', context={})


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
    QueryModel.objects.create(
        name=request.POST.get('name'), sql_statement=request.POST.get('sql_statement'))
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
    errors = []
    if not os.path.isfile(settings.CASTOR_DB_FILE) or os.path.getsize(settings.CASTOR_DB_FILE) == 0:
        errors.append(f'Database file {settings.CASTOR_DB_FILE} not found or empty. Did Prefect pipeline run?')
    if len(errors) > 0:
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
def get_query_result(request, query_id, query_result_id):
    query_result = QueryResultModel.objects.get(pk=query_result_id)
    # note: conversion to dataframe results integers in being converted to floats
    # use data dictionary to perform conversion
    df = query_result.as_df()
    return render(request, 'query_result.html', context={
        'query': query_result.query, 'query_result': query_result, 'nr_rows': len(df.index), 'columns': df.columns, 'data': df.to_numpy()})
    
    
"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def download_query_result(request, query_id, query_result_id):
    query_result = QueryResultModel.objects.get(pk=query_result_id)
    filepath = query_result.result_file
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
