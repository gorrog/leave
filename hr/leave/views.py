from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Employee

@login_required
def home_page(request):
    username = request.user.username
    context = {
            'username': username
            }
    try:
        employee = Employee.objects.get(username = username)
    except Employee.DoesNotExist:
        error_message = """
            Employee object with username {username} doesn't exist.
            Aborting...
            """
        error_message = error_message.format(username = username)
        return HttpResponse(error_message)

    context["leave_remaining"] = employee.leave_remaining
    return render(request, "home.html", context)

def login_page(request):
    if request.method == "POST":
        if request.POST.get('password') in [None,'']:
            context = {
                    'error_message': 'Password was missing or empty'
                    }
            return render(request, "login.html", context)
        if request.POST.get('username') in [None,'']:
            context = {
                    'error_message': 'Username was missing or empty'
                    }
            return render(request, "login.html", context)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                context = {
                        'error_message': 'Your user account has been disabled.'
                        }
                return render(request, "login.html", context)
        else:
            context = {
                    'error_message': "Username or Password was incorrect. Please try again"
                    }
            return render(request, "login.html", context)
    else:
        return render(request, "login.html")

@login_required
def logout_page(request):
    if request.method == "GET":
        return HttpResponseBadRequest()
    if request.method == "POST":
        logout(request)
        return redirect("/login/")

