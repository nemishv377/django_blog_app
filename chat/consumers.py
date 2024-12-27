import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room
from accounts.models import Author
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
  
  def __init__(self, *args, **kwargs):
    super().__init__(args, kwargs)
    self.room_name = None
    self.room_group_name = None
    self.room = None
    self.user = None
  
  def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'
    self.room = Room.objects.get(name=self.room_name)
    self.user = self.scope['user']

    # connection has to be accepted
    self.accept()
    
    # join the room group
    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,
      self.channel_name,
    )
    
    self.send(json.dumps({
      'type': 'user_list',
      'users': [Author.objects.get(id=id).username for id in self.room.online],
    }))
  
    if self.user.is_authenticated:
      # send the join event to the room
      async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
          'type': 'user_join',
          'user': self.user.username,
          'users': [Author.objects.get(id=id).username for id in self.room.online],
        }
      )


  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)(
      self.room_group_name,
      self.channel_name,
    )
    
    if self.user.is_authenticated:
      # send the leave event to the room
      async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
          'type': 'user_leave',
          'user': self.user.username,
          'users': [Author.objects.get(id=id).username for id in self.room.online],
        }
      )

  
  # Receive message from WebSocket
  def receive(self, text_data=None, bytes_data=None):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    current_time = datetime.now().strftime('%H:%M:%S')

    if not self.user.is_authenticated:  # new
      return   
    # send chat message event to the room
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message,
        'username': self.user.username,
        'time': current_time, 
      }
    )

  # Receive message from room group
  def chat_message(self, event):
    self.send(text_data=json.dumps(event))
    
  
  def user_join(self, event):
    self.send(text_data=json.dumps(event))

  def user_leave(self, event):
    self.send(text_data=json.dumps(event))