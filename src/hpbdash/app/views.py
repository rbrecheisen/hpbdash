import os
import json

from django.shortcuts import render
from django.views.static import serve
from django.contrib.auth.decorators import login_required

from .models import QueryModel

from barbell2.castor.castor2sqlite import CastorQuery


@login_required
def get_queries(request):
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


@login_required
def create_query(request):
    print(request.POST.get('name'))
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
    query = QueryModel.objects.get(pk=query_id)
    query_engine = CastorQuery('/tmp/castor.db')
    df = query_engine.execute(query.sql_statement)
    query_engine.to_csv('/tmp/castor_query_results.csv')
    df_array = df.to_numpy()
    return render(request, 'query_result.html', context={
        'query': query, 'nr_rows': len(df_array), 'columns': df.columns, 'data': df_array})


@login_required
def download_query_results(request, query_id):
    filepath = '/tmp/castor_query_results.csv'
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))