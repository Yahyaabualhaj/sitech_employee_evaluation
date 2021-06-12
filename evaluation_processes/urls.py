from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='evaluation_home_page'),
    path('evaluation-360-application/', views.evaluation_360_application, name='evaluation_360_application'),
    path('evaluation-360/', views.evaluation_360, name='evaluation_360'),
    path('self-evaluation/', views.self_evaluation, name='self_evaluation'),
]
