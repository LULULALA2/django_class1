#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserModel(AbstractUser): # 장고에서 제공하는 기본 모델을 수정하기 위해 UserModel에 불러옴
    class Meta:
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')
