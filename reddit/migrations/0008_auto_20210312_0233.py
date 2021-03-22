# Generated by Django 3.1.6 on 2021-03-11 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0007_auto_20210308_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='is_disliked',
            field=models.CharField(choices=[('true', 'true'), ('false', 'false'), ('none', 'none')], max_length=20),
        ),
        migrations.AlterField(
            model_name='like',
            name='is_liked',
            field=models.CharField(choices=[('true', 'true'), ('false', 'false'), ('none', 'none')], max_length=20),
        ),
        migrations.AlterField(
            model_name='posts',
            name='desc',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]