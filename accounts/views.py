from django.shortcuts import render, redirect
from .forms import AuthorSignupForm
from django.contrib.auth import login

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