from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    else:
        return render(request, "login.html")
