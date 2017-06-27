from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DbUser, DbArticle

admin.site.register(DbUser, UserAdmin)
admin.site.register(DbArticle)
