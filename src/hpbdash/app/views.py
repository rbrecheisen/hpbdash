from django.shortcuts import render

from .models import QueryModel


def get_queries(request):
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


def get_query(request, query_id):
    query = QueryModel.objects.get(pk=query_id)
    return render(request, 'query.html', context={'query': query})


def create_query(request):
    pass


def delete_query(request, query_id):
    pass