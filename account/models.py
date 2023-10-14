import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUserManager(UserManager):
    def _create_user(self, name, email, username, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def _create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, username, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_superuser(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, default='')
    name = models.CharField(max_length=255, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    follows = models.ManyToManyField( 
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_avatar(self):
        if self.avatar:
            # NOTES: this is where the issue seems to be arising
            print(settings.WEBSITE_URL)
            return settings.WEBSITE_URL + self.avatar.url
            # print(self.avatar.url)
            # return self.avatar.url
        else:
            return 'https://bulma.io/images/placeholders/128x128.png'