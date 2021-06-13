from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def register(request):
    if request.method == 'POST':
        # Get form values

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:

            # Check  username
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')

            else:
                # Check email
                if User.objects.filter(email__iexact=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')

                else:
                    # looks good
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password,

                    )
                    # Login after register.
                    # auth.login(request,user)
                    # messages.success(request,'You are now logged in')
                    # return redirect('pages:index')
                    user.save()
                    messages.success(request, 'You are now registered and you can log in')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')


    else:
        return render(request, 'accounts/register.html')


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
