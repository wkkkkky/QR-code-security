from django.contrib import admin
from .models import *


# Register your models here.

# logo信息
@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('logo_id', 'logo_name', 'logo_host',)


# 黑名单
@admin.register(Black)
class BlackAdmin(admin.ModelAdmin):
    list_display = ('black_host', 'black_level',)


# 网站安全等级
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level',)