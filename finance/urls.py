from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_transaction, name='add_transaction'),
    path('delete/', views.delete_transaction, name='delete_transaction'),
    path('list/', views.get_transactions, name='list_transactions'),
    path('stats/', views.dashboard_stats, name='dashboard_stats'),
    path('export/', views.export_excel, name='export_excel'),
]
