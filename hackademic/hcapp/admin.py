from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import db_user, db_article

admin.site.register(db_user, UserAdmin)
admin.site.register(db_article)