# Generated by Django 3.0 on 2021-02-11 20:08

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='sch_date_time',
            field=models.DateTimeField(validators=[app.models.scheduled_date_validate]),
        ),
    ]
