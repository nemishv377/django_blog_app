import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
  
  def __init__(self, *args, **kwargs):
    super().__init__(args, kwargs)
    self.room_name = None
    self.room_group_name = None
    self.room = None
    self.username = None
  
  def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'
    self.room = Room.objects.get(name=self.room_name)
    self.username = self.scope['user'].username

    # connection has to be accepted
    self.accept()
    
    # join the room group
    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,
      self.channel_name,
    )

  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)(
      self.room_group_name,
      self.channel_name,
    )

  # Receive message from WebSocket
  def receive(self, text_data=None, bytes_data=None):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    username = text_data_json["username"]
    current_time = datetime.now().strftime('%H:%M:%S')

    # send chat message event to the room
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message,
        'username': username,
        'time': current_time, 
      }
    )

  # Receive message from room group
  def chat_message(self, event):
    self.send(text_data=json.dumps(event))