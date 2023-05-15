from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_queries),
    path('queries/', views.get_queries),
    path('queries/create', views.create_query),
    path('queries/<int:query_id>/delete', views.delete_query),
    path('queries/<int:query_id>/run', views.execute_query),
    path('results/<int:result_id>/', views.get_result),
    path('results/<int:result_id>/download', views.download_result),
    path('results/<int:result_id>/delete', views.delete_result),
    path('reports/', views.get_reports),
    path('reports/create', views.create_report),
    path('reports/<int:report_id>/generate_content', views.generate_report_content),
    path('reports/<int:report_id>/delete', views.delete_report),
]