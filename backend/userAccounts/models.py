from django.db import models 
from django.contrib.auth.models import AbstractUser

# Create your models here.   

# Overrides the User Model(or table) to include accountNo and role 
class NewUser(AbstractUser):
      role= models.CharField(max_length=100,null=True)
