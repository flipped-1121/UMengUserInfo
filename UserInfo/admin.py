from django.contrib import admin

# Register your models here.
from .models import User, MrSportInfo, LDSportInfo

admin.site.register(User)
admin.site.register(MrSportInfo)
admin.site.register(LDSportInfo)
