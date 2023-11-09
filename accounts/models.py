from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, phoneNumber, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            password = password,
            phoneNumber = phoneNumber
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, phoneNumber=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
            phoneNumber=phoneNumber
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    phoneNumber = models.CharField(max_length=13)
    email = models.EmailField(max_length=50, unique=True)
    treename = models.CharField(max_length=20, null=True, blank=True)
    treephase = models.IntegerField(default=1, null=True, blank=True)
    totalWatered = models.IntegerField(default=0, null=True, blank=True)
    watered = models.IntegerField(default=0, null=True, blank=True)
    tutorial = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phoneNumber']

    def __str__(self):
        return self.email
