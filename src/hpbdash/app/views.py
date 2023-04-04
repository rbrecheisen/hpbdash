from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import QueryModel


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
    query = QueryModel.objects.get(pk=query_id)
    return render(request, 'query_result.html', context={'query_result': None})
