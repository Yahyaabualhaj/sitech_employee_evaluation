
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


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


def get_evaluation_application(request,id):
    if request.method == 'GET':
        tabs = [
            {
                'name': '',
                'text': '',
                'description': '',
                'active': '',
                'tabActivated': '',
                'questions': [],

            }
        ]
        questions = {
            'id': '',
            'name': '',
            'value': '',
            'choices': [],
            'disabled': False,
            'required': True,
        }
        return JsonResponse({'success': True, 'message': 'The form is submitted successfully'})


def post_evaluation_application(request,id):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        tabs = [
            {
                'name': '',
                'text': '',
                'description': '',
                'active': '',
                'tabActivated': '',
                'questions': [],

            }
        ]
        questions = {
            'id': '',
            'name': '',
            'value': '',
            'choices': [],
            'disabled': False,
            'required': True,
        }
        return JsonResponse({'success': True, 'message': 'The form is submitted successfully'})
