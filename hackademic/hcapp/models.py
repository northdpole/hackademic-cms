import unidecode as unidecode
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import uuid


# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class DbUser(AbstractUser, PermissionsMixin):
    UserId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField()
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(unidecode(self.username))
        super(DbUser, self).save(*args, **kwargs)


class DbClasses(models.Model):
    classId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField()
    archive = models.BooleanField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.pk:
            def save(self, *args, **kwargs):
                if not self.pk:
                    self.slug = slugify(unidecode(self.name))
                super(DbUser, self).save(*args, **kwargs)
        super(DbClasses, self).save(*args, **kwargs)


class DbChallenge(models.Model):
    challengeId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    pkg_name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(DbUser)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            def save(self, *args, **kwargs):
                if not self.pk:
                    self.slug = slugify(unidecode(self.title))
                super(DbUser, self).save(*args, **kwargs)
        super(DbChallenge, self).save(*args, **kwargs)


class DbArticle(models.Model):
    titleId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(DbUser, related_name='created_by')
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(DbUser, null=True, related_name='last_modified_by')
    ordering = models.IntegerField(null=True)
    is_published = models.NullBooleanField(null=True)

    def get_absolute_url(self):
        return reverse('hcapp:article-details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            def save(self, *args, **kwargs):
                if not self.pk:
                    self.slug = slugify(unidecode(self.title))
                super(DbUser, self).save(*args, **kwargs)
        super(DbArticle, self).save(*args, **kwargs)


class DbMenus(models.Model):
    menuId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

class DbOptions(models.Model):
    optionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    option_name = models.CharField(max_length=64, unique=True)
    option_value = models.CharField(max_length=100)

class DbPages(models.Model):
    pageId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=256, unique=True)
    file = models.CharField(max_length=256)


class DbUserChallengeToken(models.Model):
    uctId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(DbUser)
    class_id = models.ForeignKey(DbClasses)
    challenge_id = models.ForeignKey(DbChallenge)
    token = models.CharField(max_length=256)


class DbUserScore(models.Model):
    usId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(DbUser)
    challenge_id = models.ForeignKey(DbChallenge)
    class_id = models.ForeignKey(DbClasses)
    points = models.IntegerField()
    penalties_bonuses = models.TextField(null=True)


class DbScoringRule(models.Model):
    srId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge_id = models.ForeignKey(DbChallenge)
    class_id = models.ForeignKey(DbClasses)
    attempt_cap = models.IntegerField()
    attempt_cap_penalty = models.IntegerField()
    time_between_first_and_last_attempt = models.IntegerField()
    time_penalty = models.IntegerField()
    time_reset_limit_seconds = models.IntegerField()
    request_frequency_per_minute = models.IntegerField()
    request_frequency_penalty = models.IntegerField()
    experimentation_bonus = models.IntegerField()
    multiple_solution_bonus = models.IntegerField()
    banned_user_agents = models.TextField(null=True)
    banned_user_agents_penalty = models.IntegerField()
    base_score = models.IntegerField()
    first_try_solves = models.IntegerField()
    penalty_for_many_first_try_solves = models.IntegerField()


class DbChallengeAttemptCount(models.Model):
    cacId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(DbUser)
    challenge_id = models.ForeignKey(DbChallenge)
    class_id = models.ForeignKey(DbClasses)
    tries = models.IntegerField(null=True)


class DbClassChallenges(models.Model):
    ccId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge_id = models.ForeignKey(DbChallenge)
    class_id = models.ForeignKey(DbClasses)
    date_created = models.DateTimeField()


class DbClassMemberships(models.Model):
    cmId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(DbUser)
    class_id = models.ForeignKey(DbClasses)
    date_created = models.DateTimeField()


class DbMenuItems(models.Model):
    miId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=256)
    menu_id = models.ForeignKey(DbMenus)
    label = models.CharField(max_length=50)
    parent = models.IntegerField() #Not sure if this needs to be a foreignkey
    sort = models.IntegerField()
