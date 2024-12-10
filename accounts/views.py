from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorSignupForm
from django.contrib.auth import login
from blog.models import Blog
from .models import Author
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):

  if request.method == 'POST':
    form = AuthorSignupForm(request.POST)
  
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')

  else:
    form = AuthorSignupForm()

  return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
  author = request.user
  blogs = Blog.objects.filter(author=author).order_by('-created_at')

  return render(request, 'accounts/my_profile.html', {'author': author, 'blogs': blogs})