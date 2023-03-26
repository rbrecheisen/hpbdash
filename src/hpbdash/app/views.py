from django.shortcuts import render

from .models import QueryModel, ReportModel


# QUERY


def get_queries(request):
    queries = QueryModel.objects.all()
    return render(request, 'queries.html', context={'queries': queries})


def get_query(request, query_id):
    query = QueryModel.objects.get(pk=query_id)
    return render(request, 'query.html', context={'query': query})


def create_query(request):
    pass


def update_query(request, query_id):
    pass


def delete_query(request, query_id):
    pass


# REPORT


def get_reports(request):
    reports = ReportModel.objects.all()    
    return render(request, 'reports.html', context={'reports': reports})


def get_report(request, report_id):
    report = ReportModel.objects.get(pk=report_id)
    return render(request, 'report.html', context={'report': report})


def create_report(request):
    pass


def delete_report(request, report_id):
    pass
