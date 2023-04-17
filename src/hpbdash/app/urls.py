from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_queries),
    path('queries/', views.get_queries),
    path('queries/create', views.create_query),
    path('queries/<int:query_id>/delete', views.delete_query),
    path('queries/<int:query_id>/run', views.execute_query),
    path('queries/<int:query_id>/results/<int:query_result_id>/', views.get_query_result),
    path('queries/<int:query_id>/results/<int:query_result_id>/download', views.download_query_result),
    path('upload', views.upload_data_dictionary),
    path('dd/fields/', views.get_fields),
    path('dd/option_groups/', views.get_option_groups),
]