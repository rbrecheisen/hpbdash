from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_queries),
    path('queries/', views.get_queries),
    path('queries/create', views.create_query),
    path('queries/<int:query_id>/delete', views.delete_query),
    path('queries/<int:query_id>/run', views.run_query),
    path('queries/<int:query_id>/results', views.download_query_results),
    path('queries/<int:query_id>/results/show', views.show_query_results),
]