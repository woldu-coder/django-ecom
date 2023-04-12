from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(HotelType)
admin.site.register(Hotel)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)