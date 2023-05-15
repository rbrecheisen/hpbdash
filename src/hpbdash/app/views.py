import os

from django.shortcuts import render, redirect
from django.views.static import serve
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required

from .models import QueryModel, QueryResultModel, ReportModel

from barbell2_castor import CastorQueryRunner


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def get_queries(request):
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


"""-------------------------------------------------------------------------------------------------------------------
"""
@login_required
def create_query(request):
    QueryModel.objects.create(
        name=request.POST.get('name'),
        database=request.POST.get('database'),
        sql_statement=request.POST.get('sql_statement')
        )
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
    # get query
    query = QueryModel.objects.get(pk=query_id)
    # check if query database exists
    db_file = settings.CASTOR_DB_FILES[query.database]
    if not os.path.isfile(db_file) or os.path.getsize(db_file) == 0:
        return render(request, 'errors.html', context={'errors': [
            f'Database file {db_file} not found or empty. Did Prefect pipeline run?'
        ]})    
    # run query and store results in csv file
    query_runner = CastorQueryRunner(db_file)
    query_runner.execute(query.sql_statement)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    query_result_file = os.path.join(settings.CASTOR_QUERY_RESULT_DIR, f'query-{query_id}-result-{timestamp}.csv')
    query_result = QueryResultModel.objects.create(
        query=query,
        result_file=query_result_file,
    )
    query_runner.to_csv(query_result.result_file)
    # redirect to query result page
    return redirect(f'/results/{query_result.id}/')
    
    
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
    # get all queries and check which one was selectec
    queries = QueryModel.objects.all()
    selected_queries = []
    for query in queries:
        query_checkbox_id = f'{query.id}_cbx'
        if request.POST.get(query_checkbox_id, None) is not None:
            selected_queries.append(query)
    # update query SQL to include the start and end dates for this new report
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    for query in selected_queries:
        if 'WHERE' in query.sql_statement:
            items = query.sql_statement.split('WHERE')
            select = items[0]
            where_clause = items[1]
            where_clause += f'WHERE {settings.CASTOR_DATOK_NAMES[query.database]} BETWEEN "{start_date}" AND "{end_date}" {where_clause}'
            query.sql_statement = select + where_clause
            if not query.sql_statement.endswith(';'):
                query.sql_statement += ';'
        else:
            if query.sql_statement.endswith(';'):
                query.sql_statement = query.sql_statement[:-1]
            query.sql_statement += f' WHERE {settings.CASTOR_DATOK_NAMES[query.database]} BETWEEN "{start_date}" AND "{end_date}";'
        print(f'updated query (not saved): {query.sql_statement}')
    # run queries where each query results in a dataframe
    for query in selected_queries:
        query_runner = CastorQueryRunner(settings.CASTOR_DB_FILES[query.database])
        df = query_runner.execute(query.sql_statement)
        print(df)
    # create report instance
    # timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    # report = ReportModel.objects.create(name=f'report-{timestamp}', start_date=start_date, end_date=end_date)    
    return redirect('/reports/')


"""-------------------------------------------------------------------------------------------------------------------
"""
def delete_report(request, report_id):
    report = ReportModel.objects.get(pk=report_id)
    report.delete()
    return redirect('/reports/')


"""-------------------------------------------------------------------------------------------------------------------
"""
def generate_report_content(request, report_id):
    report = ReportModel.objects.get(pk=report_id)
    return render(request, 'report.html', context={'report': report})
