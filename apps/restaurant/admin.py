from django.contrib import admin
from .models import *

# Register your models here.

def make_enable(modeladmin, request, queryset):
    queryset.update(is_enable=True)
make_enable.short_description = "Seleccionar restaurantes habilitados"

def make_no_enable(modeladmin, request, queryset):
    queryset.update(is_enable=False)
make_no_enable.short_description = "Seleccionar restaurantes no habilitados"

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mobile','whatsapp','location','is_enable', 'created_at', 'last_modified']
    search_fields = ['name',]
    ordering = ['name',]
    actions = [make_enable, make_no_enable]

admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Schedule)
admin.site.register(Service)
admin.site.register(Subcategory)

class ResDiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'discount','is_enable','created_at', 'last_modified']
    search_fields = ['id',]
    ordering = ['id',]

    def save_model(self, request, obj, form, change):
        if obj.is_enable == False:
            obj.discount.is_enable = False
            obj.discount.save(update_fields=['is_enable'])
        obj.save()

admin.site.register(RestaurantDiscount,ResDiscountAdmin)