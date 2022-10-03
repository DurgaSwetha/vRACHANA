from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Here you have to import the User model from your app!
from .models import User


class MyUserAdmin(UserAdmin):
        model = User
        list_display = ('username', 'email','fullname','is_staff',
                        'is_Moderator','assigned_subject', 'assigned_project','is_admin','is_active','is_superuser','has_subscribed','dob')
        list_filter = ( 'email','username','is_Moderator','is_active','is_admin','is_superuser','has_subscribed')  
        filter_horizontal = ()                                                                                                                                         
        fieldsets =  ((None, {'fields': ('username','email','fullname')}),('Permissions', {'fields': ('is_staff','is_active','is_admin', 'is_Moderator')}),
               ('Personal', {'fields': ('has_subscribed','dob')}),
               ('Domain Info', {'fields': ('assigned_subject','assigned_project')}),
        )                      
        add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'password1', 'password2')}
        ),)
        search_fields = ('fullname','email','username' )
        ordering = ('username', )

#admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

