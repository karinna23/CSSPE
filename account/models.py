from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    
    objects = UserManager()
    
    def __str__(self):
        return self.username

class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    contact_num = models.CharField(max_length=20, null=True)
    arnis = models.BooleanField(default=False)
    volleyB = models.BooleanField(default=False)
    tTennis = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
