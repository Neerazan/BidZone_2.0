from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from src.auction.admin import ProductAdmin, ProductImageInline
from src.auction.models import Product
from src.tags.models import TaggedItem

from .models import User


# Custom User Model
@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

    add_fieldsets = (
        (
            'User Information',
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'email',
                ),
            },
        ),
    )


# Decouple tags and auction app
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
