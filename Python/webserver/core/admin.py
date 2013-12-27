from django.contrib import admin
from .models import *

class VendorAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

class GroupAdmin(admin.ModelAdmin):
    pass

class DeviceAdmin(admin.ModelAdmin):
    pass

class CommandAdmin(admin.ModelAdmin):
    pass

class UpdateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Update, UpdateAdmin)
