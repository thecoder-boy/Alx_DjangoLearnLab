from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# A class manager for the User model
class UserManager(BaseUserManager):
  def createuser(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError("Email is reqyired")
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def creater_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')
    return self.createuser(email, password, **extra_fields)




# Extending the User model to accept these additional fields
class User(AbstractUser):
  date_of_birth = models.DateField(null=True, blank=True)
  profile_photo = models.ImageField(null=True, blank=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
    return self.email

  objects = UserManager()