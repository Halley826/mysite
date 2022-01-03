from django.db import models
from django.contrib.auth.models import AbstractUser
import django
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=20,primary_key=True,db_index=True)
    password = models.CharField(max_length=100,null=False)
    name=models.CharField(max_length=50)
    id_card=models.CharField(max_length=50)
    sex=models.CharField(max_length=20)
    school=models.CharField(max_length=20)
    major=models.CharField(max_length=20)
    sclass=models.CharField(max_length=20)
    admin_data=models.DateField(blank=True,default=django.utils.timezone.now)
    is_teacher=models.BooleanField(default=False)

    def __str__(self):
        return self.name