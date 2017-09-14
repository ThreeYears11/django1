from django.contrib import admin
from .models import *
# Register your models here.
class AreaAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ["gtitle","gtype"]
    list_filter = ["gtype"]
    search_fields = ['gtitle']

admin.site.register(TypeInfo)
admin.site.register(GoodsInfo,AreaAdmin)
