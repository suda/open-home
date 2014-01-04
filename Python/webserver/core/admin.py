from django.contrib import admin

from .models import *
from .tasks import send_command

class VendorAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', ]
    list_filter = ('vendor', )

class GroupAdmin(admin.ModelAdmin):
    pass

class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'group', 'state']
    list_filter = ('group', 'product', 'state', )

def send_selected(modeladmin, request, queryset):
    for item in queryset:
        send_command.delay(item.pk)
send_selected.short_description = "Send selected commands"

class CommandAdmin(admin.ModelAdmin):
    list_display = ['device', 'added_on', 'sent_on', 'kind']
    actions = [send_selected]

class UpdateAdmin(admin.ModelAdmin):
    list_display = ['device', 'received_on', 'kind']

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Update, UpdateAdmin)
