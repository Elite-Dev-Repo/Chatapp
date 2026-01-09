from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Room, Message
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                login(request, user) 
                return redirect('index')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')


def room(request):
    rooms = Room.objects.all()
    return render(request, 'chatrooms.html', {'rooms': rooms})



def createRoom(request):   
    return render(request, 'createroom.html')

# This handles the actual chat room
def roomchat(request, roomname):
    room_details = get_object_or_404(Room, name=roomname)
    messages = Message.objects.filter(room=room_details).order_by('created_at')
    return render(request, 'room.html', {
        'room': room_details,
        'messages': messages,
        'roomname': roomname
    })

def checkview(request):
    room_name = request.POST['room_name']
    if Room.objects.filter(name=room_name).exists():
        return redirect('roomchat', roomname=room_name) # Fix redirect here
    else:
        new_room = Room.objects.create(name=room_name, creator=request.user)
        new_room.save()
        return redirect('roomchat', roomname=room_name)

# ADD THIS: This view was missing but is called by your form
def send(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        room_id = request.POST.get('room_id')
        room_obj = Room.objects.get(id=room_id)
        
        # Save using Foreign Keys
        Message.objects.create(
            content=message_content,
            room=room_obj,
            sender=request.user
        )
        return redirect('roomchat', roomname=room_obj.name)


# def getMessages(request, roomname):
#     room_details = get_object_or_404(Room, name=roomname)
#     messages = Message.objects.filter(room=room_details).order_by('created_at')
    
#     # Convert message list to a list of dictionaries for JSON
#     message_list = []
#     for msg in messages:
#         message_list.append({
#             "sender": msg.sender.username,
#             "content": msg.content,
#             "created_at": msg.created_at.strftime("%H:%M"),
#         })
#     return JsonResponse({"messages": message_list})