from colorfield.fields import ColorField
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

from django.db import models
from common.models import CommonModel


# 생일자가 고르는 테이블
class UserTable(CommonModel):
    owner = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        blank=False,
        related_name="usertable",
    )

    nickname = models.CharField(
        max_length=7,
        default="",
        blank=False,
        null=False,
    )

    tablecolor = ColorField(
        default="#000000",
        help_text="케이크를 놓을 테이블 색상을 선택하세요.",
    )

    visitor_name = models.ManyToManyField(
        "Visitor",
        blank=False,
        max_length=3,
        related_name="tables",
    )

    # pickcake = models.ManyToManyField(
    #     "Visitor",
    #     blank=False,
    #     max_length=3,
    #     related_name="tables",
    # )

    def total_visitor(self):
        return self.visitors.count()

    def __str__(self):
        return f"{self.owner}"


# 방문자의 케이크 선택
class Visitor(CommonModel):
    owner = models.ForeignKey(
        "UserTable",
        on_delete=models.CASCADE,
        related_name="visitors",
    )

    pickcake = models.PositiveIntegerField(
        choices=[
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
            (7, "7"),
            (8, "8"),
            (9, "9"),
            (10, "10"),
            (11, "11"),
            (12, "12"),
        ],
        default=1,
        blank=False,
        null=False,
    )

    visitor_name = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        help_text="방문자의 이름을 입력하세요.",
    )

    visitor_password = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        validators=[RegexValidator(r"^\d{4}$", "비밀번호는 4자리 숫자로 이루어져야합니다.")],
        help_text="비밀번호는 4자리 숫자로 이루어져야합니다.",
    )

    letter = models.TextField(
        max_length=50,
        blank=False,
        null=False,
        help_text="생일 축하 메세지를 입력하세요.",
    )

    def clean(self):
        banned_words = ["시발", "씨발", "ㅅㅂ", "ㅂㅅ", "병신"]

        for word in banned_words:
            if re.search(word, self.letter):
                raise ValidationError("금지어가 포함되어 있습니다.")

    def __str__(self) -> str:
        return self.visitor_name
