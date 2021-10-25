from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/group/to/<str:group_name>/', views.index, name='index'),
]