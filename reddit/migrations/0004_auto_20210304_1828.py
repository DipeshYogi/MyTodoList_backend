# Generated by Django 3.1.6 on 2021-03-04 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reddit', '0003_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterField(
            model_name='tags',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_tags', to='reddit.posts'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='tag',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('liked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='reddit.posts')),
            ],
        ),
    ]