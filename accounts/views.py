from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect(reverse('evaluation_dashboard'))

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
