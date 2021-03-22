# Generated by Django 3.1.6 on 2021-03-03 10:24

from django.db import migrations, models
import reddit.models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterField(
            model_name='posts',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=reddit.models.upload_to),
        ),
        migrations.AlterField(
            model_name='posts',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]