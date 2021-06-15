from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('evaluation_dashboard/', views.evaluation_dashboard, name='evaluation_dashboard'),
    path('evaluation-360-application/', views.evaluation_360_application, name='evaluation_360_application'),
    path('evaluation-360/', views.evaluation_360, name='evaluation_360'),
    path('self-evaluation/', views.self_evaluation, name='self_evaluation'),
    path('get-evaluetion-application/<int:id>/', views.get_evaluation_application, name='get_evaluation_application'),
    path('post-evaluetion-application/<int:id>/', views.post_evaluation_application, name='post_evaluation_application'),
]
