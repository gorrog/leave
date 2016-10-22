from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

@login_required
def home_page(request):
    return render(request, "home.html")

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
                # Redirect to success page
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
