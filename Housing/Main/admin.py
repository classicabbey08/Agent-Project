from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Profile, Property, SavedProperty, ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'email', 'subject', 'is_read', 'created_at')
    list_filter   = ('is_read',)
    search_fields = ('full_name', 'email', 'subject')
    readonly_fields = ('full_name', 'email', 'phone', 'subject', 'message', 'created_at')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display  = ('title', 'owner', 'location', 'price', 'status', 'created_at')
    list_filter   = ('status', 'location', 'property_type')
    search_fields = ('title', 'location')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(SavedProperty)
class SavedPropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'saved_at')