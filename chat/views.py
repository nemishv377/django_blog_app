from django.shortcuts import render, redirect
from .models import Room, Message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Create your views here.

def index_view(request):
  return render(request, 'chat/index.html', {
    'rooms': Room.objects.all(),
  })
  

@login_required
def room_view(request, room_name):
  
  try:
    room = Room.objects.get(name=room_name)
  
  except:
    messages.error(request, f"There is no channel {room_name}!")
    return redirect('chat-index')
  
  today = timezone.now().date()
  online_user_count = room.get_online_users().count()
  chats = Message.objects.filter(room=room, timestamp__date=today).order_by('-timestamp')[:10][::-1]
  content = {
    'room': room, 
    'online_user_count': online_user_count,
    'chats': chats
  }

  return render(request, 'chat/room.html', content)


@login_required
def join_room(request, room_name):
  user = request.user
  
  try:
    room = Room.objects.get(name=room_name)
  
  except:
    messages.error(request, f"There is no channel {room_name}!")
    return redirect('chat-index')
  
  current_room = Room.get_user_current_room(user)
  
  if room.is_user_in_room(user):
    
    if current_room.name == room_name:
      return redirect('chat-room', room_name = room.name)
    
    else:
      messages.error(request, f"You are already in the {current_room.name} room, first leave that room to join another.")
      return redirect('chat-index')
  
  elif current_room:
    messages.error(request, f"You are already in the {current_room.name} room, first leave that room to join another.")
    return redirect('chat-index')
  
  else: 
    room.join(request.user)
    return redirect('chat-room', room_name = room.name)


def leave_room(request, room_name):
  
  try:
    room = Room.objects.get(name=room_name)

  except:
    messages.error(request, f"There is no channel {room_name}!")
    return redirect('chat-index')

  room.leave(request.user)
  return redirect('chat-index')

@csrf_exempt 
def save_message(request, room_name):
  
  try:
    room = Room.objects.get(name=room_name)
  
  except:
    messages.error(request, f"There is no channel {room_name}!")
    return redirect('chat-index') 
  
  message_data = {
    'content' : request.POST['content'],
    'sender' : request.user,
    'room' : room
  }
  sender = request.user
  print(sender)
  print(room_name)
  print(request.POST["content"])
  Message.objects.create(**message_data)
  return redirect('chat-index')
  
  
