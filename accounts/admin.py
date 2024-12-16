from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Author

def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, _("Selected users have been deactivated."))


def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, _("Selected users have been activated."))


def make_superuser(modeladmin, request, queryset):
    queryset.update(is_staff=True, is_superuser=True)
    modeladmin.message_user(request, _("Selected users have been made superusers."))


class AuthorAdmin(UserAdmin):
    model = Author
    list_display = ('username', 'email', 'first_name', 'last_name', 'state', 'city', 'joining_date', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('gender', 'is_active', 'is_staff', 'joining_date', 'state', 'city')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-joining_date',)

    # `fieldsets` for update existing user
    fieldsets = (
        ('Password Change', {
            'fields': ('password',)
        }),
        ('Personal Info', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'state', 'city',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Groups', {
            'fields': ('groups',)
        }),
        ('Important Dates', {
            'fields': ('last_login',)
        }),
    )

    # `add_fieldsets` for creating a new user
    add_fieldsets = (
        ('Author Information', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'date_of_birth', 'state', 'city', 'joining_date', 'last_login', 'is_active', 'is_staff', 'is_superuser', ),
        }),
    )
    
    actions = [activate_users, deactivate_users, make_superuser]


admin.site.register(Author, AuthorAdmin)
