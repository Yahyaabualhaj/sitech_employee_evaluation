
from django.urls import path
from evaluation_processes import views

urlpatterns = [
    path('', views.home,name='evaluation_home_page'),
    path('evaluation-360/', views.evaluation_360,name='evaluation_360'),
]
