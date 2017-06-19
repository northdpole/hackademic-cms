from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.
from django.urls import reverse


class db_user(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, null=False, unique=True)
    full_name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    joined = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True, null=True)
    is_activated = models.NullBooleanField(null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    type = models.IntegerField()
    token = models.IntegerField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name', 'type']

    def create_superuser(self, username, email, fullname, password):
        u = self.create_user(username, email, fullname, password)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)

        return u

    def __str__(self):
        return self.username

class db_challenge(models.Model):
    title = models.CharField(max_length=100, unique=True)
    pkg_name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(db_user)
    category = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=20, default="private")
    publish = models.IntegerField(default=0, null=True)
    abstract = models.CharField(max_length=50, null=True)
    level = models.CharField(max_length=50, null=True)
    duration = models.IntegerField(null=True)
    goal = models.TextField(null=True)
    solution = models.TextField(null=True)
    availability = models.CharField(max_length=50, default='private')
    default_points = models.IntegerField(null=True)
    default_duration = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse('hcapp:challenge-details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class db_article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(db_user, related_name='created_by')
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(db_user, null=True, related_name='last_modified_by')
    ordering = models.IntegerField(null=True)
    is_published = models.NullBooleanField(null=True)

    def get_absolute_url(self):
        return reverse('hcapp:article-details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title