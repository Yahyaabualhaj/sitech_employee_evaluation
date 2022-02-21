from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('evaluation_dashboard/', views.evaluation_dashboard, name='evaluation_dashboard'),
    path('evaluation-360-application/<int:team_member_id>/', views.evaluation_360_application, name='evaluation_360_application'),
    path('evaluation-360/', views.evaluation_360, name='evaluation_360'),
    path('self-evaluation/', views.self_evaluation, name='self_evaluation'),
    path('get-evaluetion-application/', views.get_evaluation_application, name='get_evaluation_application'),
    path('get-teammates/', views.get_teammates, name='get_teammates'),
    path('post-evaluetion-application/', views.post_evaluation_application, name='post_evaluation_application'),
]
