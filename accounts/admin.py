from django.contrib import admin

from .models import Purchase, Pricing, Invoice


# Register your models here.
admin.site.register(Purchase)
admin.site.register(Pricing)
admin.site.register(Invoice)
