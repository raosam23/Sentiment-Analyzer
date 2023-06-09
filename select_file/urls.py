from django.urls import path
from . import views

urlpatterns = [
    path("", views.select, name="select-file"),
    path("selected", views.selected_file, name="selected-file"),
    path("select_algo", views.choose_algorithm, name="choose-algorithm"),
]