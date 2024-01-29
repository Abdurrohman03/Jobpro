from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import pre_save, post_save
from datetime import datetime
from dateutil import relativedelta


class Company(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class Country(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


class City(models.Model):
    title = models.CharField(max_length=225)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, {self.country.title}'


class Position(models.Model):
    title = models.CharField(max_length=225)

    def __str__(self):
        return self.title


def image_path(instance, filename):
    return f'accounts/{instance.id}/{filename}'


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have email')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be None')

        user = self.create_user(username=username, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.role = 2
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        (0, 'Candidate'),
        (1, 'HR'),
        (2, 'Stuff'),
    )
    username = models.CharField(max_length=225, unique=True)
    email = models.EmailField(max_length=50, unique=True, verbose_name='Email', db_index=True, null=True)
    first_name = models.CharField(max_length=50, verbose_name='First name', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Last name', null=True)
    image = models.ImageField(upload_to=image_path, null=True, blank=True)
    bio = models.TextField()
    full_name = models.CharField(max_length=50, verbose_name='Full name', null=True)
    phone = models.CharField(max_length=16, verbose_name='Phone Number', null=True)
    stack = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    role = models.IntegerField(choices=ROLE, default=0)
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_staff = models.BooleanField(default=False, verbose_name='Staff user')
    is_active = models.BooleanField(default=True, verbose_name='Active user')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created')

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.last_name} {self.first_name}'
        return f'{self.username}'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"> <img src="{self.image.url}" style="height:150px;"/> </a>' )
        return 'Image not found'

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            return f'{settings.PROD_BASE_URL}{self.image.url}'
        return None

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


class WorkHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(null=True, blank=True)

    @property
    def work_experience(self):
        delta = relativedelta.relativedelta(self.end_date, self.start_date)
        return f'{delta.years} Years, {delta.months} months, {delta.days}, days'


def account_pre_save(instance, sender, *args, **kwargs):
    if instance.role == 2:
        instance.is_staff = True
    else:
        instance.is_staff = False
    return instance


pre_save.connect(account_pre_save, sender=Account)
