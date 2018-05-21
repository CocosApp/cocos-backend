from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# Register your models here.

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'picture', 'is_active', 'birthday','is_admin_res', 'cellphone','ruc','business_name')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        # (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
        #                                'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_admin_res'),
        }),
    )
    list_display = ('id', 'email','first_name','last_name','cellphone','is_admin_res', 'is_active', 'created_at', 'last_modified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups','is_admin_res')
    search_fields = ('first_name', 'last_name', 'email',)
    ordering = ('first_name','email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User,MyUserAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaurant','created_at', 'last_modified']
    search_fields = ['name']

admin.site.register(UserRestaurant,RestaurantAdmin)

class UserAdminRestaurantAdmin(admin.ModelAdmin):
    model = UserAdminRestaurant
    list_display = ['id', 'user','restaurant','is_enable', 'created_at', 'last_modified']
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        if obj.is_enable == True:
            obj.user.is_enabled = True
            obj.restaurant.is_enable=True
            obj.user.save(update_fields=['is_enabled'])
            obj.restaurant.save(update_fields=['is_enable'])
        obj.save()

admin.site.register(UserAdminRestaurant,UserAdminRestaurantAdmin)