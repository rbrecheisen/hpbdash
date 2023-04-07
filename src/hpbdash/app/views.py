import os
import json
import pandas as pd

from django.shortcuts import render
from django.views.static import serve
from django.contrib.auth.decorators import login_required

from .models import QueryModel

from barbell2.castor.castor2sqlite import CastorQuery

CASTOR_DB = '/tmp/castor.db'
CASTOR_QUERY_RESULTS = '/tmp/castor_query_results.csv'


@login_required
def get_queries(request):
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


@login_required
def create_query(request):
    QueryModel.objects.create(
        name=request.POST.get('name'), sql_statement=request.POST.get('sql_statement'))
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


@login_required
def delete_query(request, query_id):
    query = QueryModel.objects.get(pk=query_id)
    query.delete()
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


@login_required
def run_query(request, query_id):
    # 'SELECT dpca_datok FROM data WHERE dpca_datok BETWEEN "2018-05-01" AND "2018-07-01";'
    errors = []
    if not os.path.isfile(CASTOR_DB) or os.path.getsize(CASTOR_DB) == 0:
        errors.append(f'Database file {CASTOR_DB} not found or empty. Did Prefect pipeline run?')
    if len(errors) > 0:
        return render(request, 'errors.html', context={'errors': errors})    
    query_engine = CastorQuery(CASTOR_DB)
    query = QueryModel.objects.get(pk=query_id)
    df = query_engine.execute(query.sql_statement)
    query_engine.to_csv(CASTOR_QUERY_RESULTS)
    df_array = df.to_numpy()
    return render(request, 'query_results.html', context={
        'query': query, 'nr_rows': len(df_array), 'columns': df.columns, 'data': df_array})
    
    
@login_required
def show_query_results(request, query_id):
    query = QueryModel.objects.get(pk=query_id)
    df = pd.read_csv(CASTOR_QUERY_RESULTS)
    for column in df.columns:
        if request.POST.get(f'{column}_cbx', None) is not None:
            print('Found selected column!')
    return render(request, 'show_query_results.html', context={'query': query})


@login_required
def download_query_results(request, query_id):
    filepath = CASTOR_QUERY_RESULTS
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))