from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class IsStaff(permissions.BasePermission):

  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.is_staff



schema_view = get_schema_view(
  openapi.Info(
    title="Django Blog App",
    default_version='v1',
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@myapi.local"),
    license=openapi.License(name="BSD License"),
  ),
  public=True,
  permission_classes=(IsStaff,),
)