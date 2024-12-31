from django.contrib import admin
from .models import Room, Message

# Register your models here.
class MeesageAdmin(admin.ModelAdmin):
  model = Message
  list_display = ('content', 'sender', 'room', 'timestamp')  
  list_filter = ('room',)    
  search_fields = ('sender__username', 'content')

admin.site.register(Room)
admin.site.register(Message, MeesageAdmin)