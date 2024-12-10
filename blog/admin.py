from django.contrib import admin
from .models import Blog

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
  model = Blog
  list_display = ('title', 'author', 'created_at', 'updated_at', 'image')  
  list_filter = ('author', 'created_at')    
  search_fields = ('title', 'content')

  fields = ('title', 'content', 'author', 'image')

  readonly_fields = ('created_at', 'updated_at')


admin.site.register(Blog, BlogAdmin)