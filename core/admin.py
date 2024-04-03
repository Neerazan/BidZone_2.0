from django.contrib import admin
from .models import User
from auction.admin import ProductAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from auction.models import Product
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#Custom User Model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            "User Information",
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "password1", "password2", "email"),
            },
        ),
    )


#Decouple tags and auction app
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)