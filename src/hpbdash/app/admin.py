from django.contrib import admin
from .models import QueryModel


@admin.register(QueryModel)
class QueryModelAdmin(admin.ModelAdmin):
    list = (
        'title',
        'sql_statement',
    )