from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.core.paginator import Paginator

# Create your views here.

def blogs_list(request):
  blogs = Blog.objects.all().order_by('-created_at')
  paginator = Paginator(blogs, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'blog/blogs_list.html', {'page_obj': page_obj})
  
def blog_detail(request, id):
  blog = get_object_or_404(Blog, id=id)
  return render(request, 'blog/blog_detail.html', {'blog': blog})