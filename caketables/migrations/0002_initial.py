# Generated by Django 4.2.1 on 2023-07-20 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('caketables', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertable',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usertable', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usertable',
            name='visitor_name',
            field=models.ManyToManyField(max_length=3, related_name='tables', to='caketables.visitor'),
        ),
    ]