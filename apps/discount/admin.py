from django.contrib import admin
from .models import *

# Register your models here.
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','promotion', 'porc', 'price','is_enable','card','created_at','finished_at']
    search_fields = ['name']
    ordering = ['-id',]

    def save_model(self, request, obj, form, change):
        if obj.is_enable == False:
            for discount in obj.res_discount.all():
                print(obj)
                print(obj.is_enable)
                if obj.is_enable == False:
                    print(obj)
                    print(obj.res_discount.first())
                    obj.res_discount.first().delete()
                    obj.is_enable = False
                    obj.save(update_fields=['is_enable'])
                obj.save()
            obj.save()
        if obj.is_enable == True:
            obj.save()

admin.site.register(Discount,DiscountAdmin)
admin.site.register(Card)