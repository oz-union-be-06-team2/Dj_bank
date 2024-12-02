from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, nickname, phone_num, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            nickname=nickname,
            phone_num=phone_num,
            **extra_fields
        )
        user.set_password(password)
        user.is_active = True  # 또는 False로 설정하여 이메일 인증 추가 가능
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, nickname, phone_num, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email,
            name,
            nickname,
            phone_num,
            password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    # 모든 필드를 직접 정의해야 함
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, unique=True, null=True)
    phone_num = models.CharField(max_length=15, unique=True, null=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # 직접 추가해야 할 필드들
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname', 'phone_num']

    def __str__(self):
        return self.email