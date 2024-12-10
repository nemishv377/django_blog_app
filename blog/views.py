from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from accounts.models import Author
from django.core.paginator import Paginator
from .forms import BlogForm
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def new_blog(request):

  if request.method == 'POST':
    form = BlogForm(request.POST, request.FILES)

    if form.is_valid():
      blog = form.save(commit=False)
      blog.author = request.user
      blog.save() 
      return redirect('blogs_list')

    else:
      return render(request, 'blog/new_blog.html', {'form': form})

  else:
    form = BlogForm()

  return render(request, 'blog/new_blog.html', {'form': form})


@login_required
def delete_blog(request, id):
  blog = get_object_or_404(Blog, id=id)

  if blog.author != request.user:
    return redirect('profile')  # Or an error page if not the author

  if request.method == 'POST':
    blog.delete()
    return redirect('profile')

  return redirect('profile')


def blogs_list(request):
  blogs = Blog.objects.all().order_by('-created_at')
  paginator = Paginator(blogs, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, 'blog/blogs_list.html', {'page_obj': page_obj})
  

def blog_detail(request, id):
  blog = get_object_or_404(Blog, id=id)

  return render(request, 'blog/blog_detail.html', {'blog': blog})


def bloggers_list(request):
  bloggers = Author.objects.all()

  return render(request, 'blog/bloggers_list.html', {'bloggers': bloggers})


def blogger_detail(request, id):
  author = get_object_or_404(Author, id=id)
  blogs = Blog.objects.filter(author=author).order_by('-created_at')

  return render(request, 'blog/blogger_detail.html', {'author': author, 'blogs': blogs})


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
      return redirect('blog_detail', id=blog.id)
    
  else:
    form = CommentForm()

  return render(request, 'blog/create_comment.html', {'form': form, 'blog': blog})