from django.urls import path
from . import views

urlpatterns = [
    path("", views.support_vector, name='Support-Vector'),
    path("compute_support_vector", views.compute_support_vector, name = 'Compute-Support-Vector'),
]