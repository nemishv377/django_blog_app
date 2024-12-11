from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorSignupForm
from django.contrib.auth import login, logout, authenticate
from blog.models import Blog
from .models import Author
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .utils import get_user_permissions

# Create your views here.

def custom_login_view(request):

  if request.user.is_authenticated:
    messages.success(request, 'You have already logged in!')
    return redirect('home')
 
  next_url = request.GET.get('next') or request.POST.get('next')
  next_url = 'home' if next_url is None else next_url
  
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
      user = form.get_user()
      login(request, user)
      messages.success(request, 'You have successfully logged in!')
      return redirect(next_url) if next_url else redirect('home')

  else:
    form = AuthenticationForm()
    
  content = {
    'form': form,
    'next_url': next_url
  }

  return render(request, 'registration/login.html', content)


def signup(request):

  if request.user.is_authenticated:
    messages.success(request, 'You have already logged in!')
    return redirect('home')

  if request.method == 'POST':
    form = AuthorSignupForm(request.POST)

    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, 'You have successfully signed up and are now logged in!')
      return redirect('home')

  else:
    form = AuthorSignupForm()

  return render(request, 'accounts/signup.html', {'form': form})


def custom_logout_view(request):
  logout(request)
  messages.info(request, 'You have successfully logged out.')
  return redirect('login')


@login_required
def profile(request):
  author = request.user
  blogs = Blog.objects.filter(author=author).order_by('-created_at')
  user_has_perm = get_user_permissions(request.user)
  content = {
    'author': author,
    'blogs': blogs,
    **user_has_perm  
  }

  return render(request, 'accounts/my_profile.html', content)


@login_required
def register(request):

  if request.user.has_perm('author.can_add_author'):

    if request.method == 'POST':
      form = AuthorSignupForm(request.POST)

      if form.is_valid():
        user = form.save()
        messages.success(request, f'{user.username} have successfully registered!')
        return redirect('home')

    else:
      form = AuthorSignupForm()
    
    user_has_perm = get_user_permissions(request.user)
    content = {
      'form': form,
      **user_has_perm  
    }

    return render(request, 'accounts/signup.html', content)

  else:
    messages.error(request, "You are not authorized to access that page!")
    return redirect('home')
