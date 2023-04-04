from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_queries),
    path('queries/', views.get_queries),
    path('queries/<int:query_id>/', views.get_query),
    path('queries/create', views.create_query),
    path('queries/<int:query_id>/delete', views.delete_query),
]