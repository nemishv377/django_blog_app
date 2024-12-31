from django.db import models
from accounts.models import Author
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Room(models.Model):
  name = models.CharField(max_length=128)
  online = ArrayField(models.IntegerField(), default=list, blank=True)
  
  @classmethod
  def get_user_current_room(cls, user):
    return cls.objects.filter(online__contains=[user.id]).first()

  def is_user_in_room(self, user):
    return user.id in self.online


  def get_online_users(self):
    return Author.objects.filter(id__in=self.online)


  def get_online_count(self):
    return len(self.online)


  def join(self, user):
    if user not in self.online:
      self.online.append(user.id)
      self.save()


  def leave(self, user):
    if user.id in self.online:
      self.online = list(set(self.online) - {user.id})
      self.save()


  class Meta:
    db_table = 'room' 


  def __str__(self):
    return f'{self.name}'


class Message(models.Model):
  sender = models.ForeignKey(Author, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  content = models.CharField(max_length=512)
  timestamp = models.DateTimeField(auto_now_add=True)


  class Meta:
    db_table = 'message' 


  def __str__(self):
    return f'{self.sender.username}: {self.content} [{self.timestamp}]'