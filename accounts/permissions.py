from rest_framework import permissions


class IsAuthorPermission(permissions.BasePermission):

  def has_permission(self, request, view):
    
    if request.user and request.user.is_authenticated:
      
      if request.user.groups.filter(name="Admin").exists():
      
        if request.method in ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']:

          if 'http://localhost:8000/api/blog/bloggers/' in request.build_absolute_uri():
            return True
          
          print(request.build_absolute_uri())
          print('http://localhost:8000/api/blog/blogs/' in request.build_absolute_uri())
          if 'http://localhost:8000/api/blog/blogs/' in request.build_absolute_uri():
            return True
          
          if 'http://localhost:8000/api/accounts/register/' in request.build_absolute_uri():
            return True
    
    else:
      return False
      
    if request.method in permissions.SAFE_METHODS:
      return True
      
    return False
