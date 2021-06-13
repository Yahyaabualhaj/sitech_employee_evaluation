from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'evaluation_processes/home.html')


def evaluation_dashboard(request):
    return render(request, 'evaluation_processes/evaluation_dashboard.html')


@login_required
def evaluation_360_application(request):
    return render(request, 'evaluation_processes/evaluation_360_application.html')


@login_required
def evaluation_360(request):
    return render(request, 'evaluation_processes/evaluation_360_main_page.html')


def self_evaluation(request):
    return render(request, 'evaluation_processes/self_evaluation.html')
