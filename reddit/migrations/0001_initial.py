# Generated by Django 3.1.6 on 2021-03-03 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import reddit.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('desc', models.CharField(blank=True, max_length=250)),
                ('img', models.ImageField(null=True, upload_to=reddit.models.upload_to)),
                ('created_on', models.DateField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]