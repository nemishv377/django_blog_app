from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from accounts.models import Author
from django.core.paginator import Paginator
from .forms import BlogForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.utils import get_user_permissions

# Create your views here.

def home(request):
  
  if request.user.is_authenticated:
    content = get_user_permissions(request.user)
  
  else:
    content = {}
    
  return render(request, 'home.html',content)


@login_required
def new_blog(request):
  
  if not request.user.has_perm('blog.add_blog'):
    messages.info(request, 'You are not authorized to that page!')
    return redirect('home')
  
  if request.method == 'POST':
    form = BlogForm(request.POST, request.FILES)

    if form.is_valid():
      blog = form.save(commit=False)
      blog.author = request.user
      blog.save() 
      messages.success(request, 'Your blog has been created successfully!')
      return redirect('blogs_list')

  else:
    form = BlogForm()
  
  user_has_perm = get_user_permissions(request.user)
  content = {
    'form': form,
    **user_has_perm  
  }

  return render(request, 'blog/new_blog.html', content)


@login_required
def delete_blog(request, id):
  blog = get_object_or_404(Blog, id=id)
  
  if request.user.has_perm('blog.can_delete_blog') and request.method == 'POST':
    messages.success(request, "Blog deleted successfully!")
    blog.delete()
  
  else:
    messages.error(request, "You are not authorized to access that page!")

  return redirect('profile')


def blogs_list(request):
  blogs = Blog.objects.all().order_by('-created_at')
  paginator = Paginator(blogs, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  user_has_perm = get_user_permissions(request.user)
  content = {
    'page_obj': page_obj,
    **user_has_perm  
  }

  return render(request, 'blog/blogs_list.html', content)
  

def blog_detail(request, id):
  blog = get_object_or_404(Blog, id=id)
  user_has_perm = get_user_permissions(request.user)
  content = {
    'blog': blog,
    **user_has_perm  
  }

  return render(request, 'blog/blog_detail.html', content)


def bloggers_list(request):
  bloggers = Author.objects.all()
  user_has_perm = get_user_permissions(request.user)
  content = {
    'bloggers': bloggers,
    **user_has_perm  
  }

  return render(request, 'blog/bloggers_list.html', content)


def blogger_detail(request, id):
  author = get_object_or_404(Author, id=id)
  blogs = Blog.objects.filter(author=author).order_by('-created_at')
  user_has_permission = request.user.has_perm('blog.add_blog')
  user_has_perm = get_user_permissions(request.user)
  content = {
    'author': author,
    'blogs': blogs,
    **user_has_perm  
  }

  return render(request, 'blog/blogger_detail.html', content)


@login_required
def create_comment(request, blog_id):
  blog = get_object_or_404(Blog, id=blog_id)

  if request.method == 'POST':
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.blog = blog
      comment.author = request.user
      comment.save()
      messages.success(request, 'Your comment has been posted successfully!')
      return redirect('blog_detail', id=blog.id)

  else:
    form = CommentForm()

  user_has_perm = get_user_permissions(request.user)
  content = {
    'form': form,
    'blog': blog,
    **user_has_perm  
  }
  
  return render(request, 'blog/create_comment.html', content)