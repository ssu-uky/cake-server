from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from common.models import CommonModel
from django.core.validators import RegexValidator

import re
from rest_framework.exceptions import ParseError, ValidationError


class User(AbstractUser):
    username = None

    name = models.CharField(
        max_length=7,
        blank=False,
        validators=[MinLengthValidator(2, "이름은 두 글자 이상이여야합니다.")],
    )

    email = models.EmailField(
        blank=False, unique=True, error_messages={"unique": "이미 존재하는 이메일입니다."}
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)  # 이메일 인증 확인

    # birthday = models.DateField(blank=False, null=False)

    SOCIAL_TYPE_CHOICES = (
        ("email", "Email"),
        ("kakao", "Kakao"),
        # ("naver", "Naver"),
    )
    social_type = models.CharField(
        max_length=10, choices=SOCIAL_TYPE_CHOICES, default="Email"
    )

    def __str__(self):
        return self.name


class FeedbackUser(CommonModel):
    feedback_name = models.CharField(max_length=7, blank=False)
    feedback_email = models.EmailField(blank=False)
    feedback_content = models.TextField(max_length=50, blank=False)
    feedback_password = models.CharField(max_length=8, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.feedback_name
