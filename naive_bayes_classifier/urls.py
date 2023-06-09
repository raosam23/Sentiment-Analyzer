from django.urls import path
from . import views
urlpatterns = [
    path("", views.naive_bayes, name="Naive-Bayes"),
    path("compute_naive_bayes", views.compute_naive_bayes, name="Compute-Naive-Bayes"),
]