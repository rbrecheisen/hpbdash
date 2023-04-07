import os

from django.shortcuts import render
from django.views.static import serve
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from .models import QueryModel, QueryResultModel

from barbell2.castor.castor2sqlite import CastorQuery


@login_required
def upload_data_dictionary(request):
    """ Processes upload of a Castor export file and extracts a dictionary of all option variables and their values
    See scripts-ralph code for an example of building COLUMN_META_DATA. Just go through list of study variables and
    take those that are option groups. Then lookup the option values in the next sheet.
    Perhaps store the lookup table efficiently using NumPy? Or pickle? JSON?
    """
    f = request.FILES.get('file')
    if isinstance(f, TemporaryUploadedFile):
        f_path = f.temporary_file_path
        print(f'TemporaryUploadedFile: {f_path}')
    elif isinstance(f, InMemoryUploadedFile):
        f_path = os.path.join(settings.MEDIA_ROOT, default_storage.save(f.name, ContentFile(f.read())))
        print(f'InMemoryUploadedFile: {f_path}')
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


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
    if not os.path.isfile(settings.CASTOR_DB_FILE) or os.path.getsize(settings.CASTOR_DB_FILE) == 0:
        errors.append(f'Database file {settings.CASTOR_DB_FILE} not found or empty. Did Prefect pipeline run?')
    if len(errors) > 0:
        return render(request, 'errors.html', context={'errors': errors})    
    query_engine = CastorQuery(settings.CASTOR_DB_FILE)
    query = QueryModel.objects.get(pk=query_id)
    df = query_engine.execute(query.sql_statement)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    query_result_file = os.path.join(settings.CASTOR_QUERY_RESULT_DIR, f'query-{query_id}-result-{timestamp}.csv')
    query_result = QueryResultModel.objects.create(
        query=query,
        result_file=query_result_file,
    )
    query_engine.to_csv(query_result.result_file)
    df_array = df.to_numpy()
    return render(request, 'query_result.html', context={
        'query': query, 'query_result': query_result, 'nr_rows': len(df_array), 'columns': df.columns, 'data': df_array})
    
    
@login_required
def get_query_result(request, query_id, query_result_id):
    query_result = QueryResultModel.objects.get(pk=query_result_id)
    df = query_result.as_df()
    df_array = df.to_numpy()
    return render(request, 'query_result.html', context={
        'query': query_result.query, 'query_result': query_result, 'nr_rows': len(df_array), 'columns': df.columns, 'data': df_array})
    
    
@login_required
def show_query_result(request, query_id, query_result_id):
    query_result = QueryResultModel.objects.get(pk=query_result_id)
    df = query_result.as_df()
    for column in df.columns:
        if request.POST.get(f'{column}_cbx', None) is not None:
            print('Found selected column!')
    return render(request, 'show_query_result.html', context={})


@login_required
def download_query_result(request, query_id, query_result_id):
    query_result = QueryResultModel.objects.get(pk=query_result_id)
    filepath = query_result.result_file
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
