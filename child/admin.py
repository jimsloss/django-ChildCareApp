from django.contrib import admin

from .models import Child
from .models import Parent
from .models import Attendance

# Register your models here.
admin.site.register(Child)
admin.site.register(Parent)
admin.site.register(Attendance)
