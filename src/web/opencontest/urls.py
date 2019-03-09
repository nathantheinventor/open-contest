from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('problems', views.list_problems),
    path('problems/<int:id>', views.view_problem),
    path('submit', views.submit),
]
