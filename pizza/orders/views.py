from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import MenuItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        username = None
    else:
        username = request.user

    context = {
        "items": MenuItem.objects.all(),
        "username": username
    }

    return render(request, "orders/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    context = {
        "items": MenuItem.objects.all(),
        "message": "invalid password"
    }

    return render(request, "orders/index.html", context)

def logout_view(request):
    logout(request)

    context = {
        "items": MenuItem.objects.all(),
        "message": "logged out"
    }
    return render(request, "orders/index.html", context)

def create_account(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.create_user(username, email, password)
            return render(request, "orders/index.html")
        except:
            return HttpResponse("User already exists")

    else:
        return render(request, "orders/create_account.html")
