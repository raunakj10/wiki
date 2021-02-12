from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.title,name="title"),
    path("search",views.search,name="search"),
    path("newpage",views.newpage,name="newpage"),
    path("edit/<str:title>/",views.edit,name="edit"),
    path("random", views.random_function, name="random")
]
