from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


def loginUser(request):
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    return render(request, 'register.html')

def chatRooms(request):
    return render(request, 'chatrooms.html')
