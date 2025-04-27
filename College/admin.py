from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class QueryFormAdmin(ImportExportModelAdmin):
    list_display=['Name','MobileNumber','Department','Venue','Floor','RoomNo','Complaint','Status','Date','Remark']
admin.site.register(QueryForm,QueryFormAdmin)
admin.site.register([Login,GuestLogin,AdminLogin]) 
