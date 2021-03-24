from django.contrib import admin

# Register your models here.


from .models import Feet, Leg, Table
# ...
admin.site.register(Feet)
admin.site.register(Leg)
admin.site.register(Table)