import re

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import UserTable, Visitor

from rest_framework import serializers


# visitor name 조회 // 제일 상단에 있어야 하위에서 인식
class AllVisitorSerializer(ModelSerializer):
    class Meta:
        model = Visitor
        fields = (
            "pk",
            "visitor_name",
            "visitor_password",
            "pickcake",
            "letter",
        )


# User 간단히 조회 및 선택 시 사용
class UserMiniSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields = ("nickname",)


# 모두가 볼 수 있는 user table
# [get] == OK
class TableShowSerializer(ModelSerializer):
    visitors = AllVisitorSerializer(many=True, read_only=True)
    user_pk = serializers.PrimaryKeyRelatedField(source="owner", read_only=True)

    class Meta:
        model = UserTable
        fields = (
            "user_pk",
            "nickname",
            "tablecolor",
            "visitors",  # 방문자 이름들
            "total_visitor",
        )
        read_only_fields = ("__all__",)


# 유저가 테이블 생성할 때 사용
# [post] == OK
class CreateTableSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields = ("owner", "nickname", "tablecolor")
        read_only_fields = ("owner",)


# visitor 가 테이블에 방문할 때 사용
# [get / post]
class VisitorSerializer(ModelSerializer):
    nickname = UserMiniSerializer(read_only=True)
    visitor_password = serializers.CharField(write_only=True)
    letter = serializers.CharField(write_only=True)

    class Meta:
        model = Visitor
        fields = (
            "pk",
            "owner",
            "nickname",
            "pickcake",
            "letter",
            "visitor_name",
            "visitor_password",
        )
        read_only_fields = (
            "pk",
            "owner",
            "nickname",
        )
        write_only_fields = (
            # "visitor_password",
            "letter",
        )

    def validate(self, data):
        letter = data.get("letter")
        banned_words = ["시발", "씨발", "ㅅㅂ", "ㅂㅅ", "병신"]

        for word in banned_words:
            if word in letter:
                raise serializers.ValidationError("금지어가 포함되어 있습니다.")

        return data


# 유저가 테이블 조회 및 삭제할 때 사용
# [get / delete]
class UserTableSerializer(ModelSerializer):
    visitors = VisitorSerializer(many=True, read_only=True)
    total_visitor = SerializerMethodField()

    class Meta:
        model = UserTable
        fields = (
            "pk",
            "nickname",
            "tablecolor",
            "visitors",
            "total_visitor",
        )
        read_only_fields = (
            "pk",
            "nickname",
            "total_visitor",
        )

    def get_total_visitor(self, obj):
        return obj.visitors.count()


# 편지 조회 / 삭제 시 사용
class LetterSerializer(ModelSerializer):
    # visitor_password = serializers.CharField(write_only=True)

    class Meta:
        model = Visitor
        fields = (
            "pk",
            "visitor_name",
            "visitor_password",
            "letter",
        )
