from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'evaluation_processes/home.html')

def evaluation_360(request):
    return render(request,'evaluation_processes/evaluation_360_form.html')