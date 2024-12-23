from django.contrib import admin
from .models import Blog, Comment
from django.utils.html import format_html

# Register your models here.

class CommentInline(admin.TabularInline):
  model = Comment
  extra = 1
  fields = ('author', 'message', 'created_at',)
  readonly_fields = ('created_at',)


class BlogAdmin(admin.ModelAdmin):
  model = Blog
  list_display = ('title', 'author', 'created_at', 'updated_at', 'image')  
  list_filter = ('author', 'created_at')    
  search_fields = ('title', 'content')
  fields = ('title', 'content', 'author', 'image')
  readonly_fields = ('created_at', 'updated_at')
  inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
  model = Comment
  list_display = ('short_message', 'author', 'blog', 'created_at')  
  list_filter = ('author', 'blog', 'created_at')    
  search_fields = ('message',)
  fields = ('message', 'author', 'blog')
  readonly_fields = ('created_at', 'updated_at')


  def short_message(self, obj):

    if len(obj.message) > 20:
      return format_html('<span title="{}">{}...</span>', obj.message, obj.message[:75])

    else:
      return format_html('<span title="{}">{}</span>', obj.message, obj.message[:75])  


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)