# Generated by Django 4.2.1 on 2023-07-20 17:54

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('nickname', models.CharField(default='', max_length=7)),
                ('tablecolor', colorfield.fields.ColorField(default='#000000', help_text='케이크를 놓을 테이블 색상을 선택하세요.', image_field=None, max_length=18, samples=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('pickcake', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')], default=1)),
                ('visitor_name', models.CharField(help_text='방문자의 이름을 입력하세요.', max_length=3)),
                ('visitor_password', models.CharField(help_text='비밀번호는 4자리 숫자로 이루어져야합니다.', max_length=8, validators=[django.core.validators.RegexValidator('^\\d{4}$', '비밀번호는 4자리 숫자로 이루어져야합니다.')])),
                ('letter', models.TextField(help_text='생일 축하 메세지를 입력하세요.', max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitors', to='caketables.usertable')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]