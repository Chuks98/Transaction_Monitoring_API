from django.urls import path
from . import views

urlpatterns = [
    path('api/transactions/create/', views.process_transaction, name='create_transaction'),
    path('api/users/<str:user>/flagged/', views.is_user_flagged, name='check_user_flagged'),
    path('api/transactions/process/', views.process_transaction, name='process_transaction'),
]
