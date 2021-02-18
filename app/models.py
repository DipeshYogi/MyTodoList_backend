from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime
import pytz


# field validators
def scheduled_date_validate(value):
  if value <= pytz.UTC.localize(datetime.datetime.now()):
    raise ValidationError('Scheduled date & time should be greater than \
                           current date & time')
  else:
    return value


class Tasks(models.Model):
  """
    Tasks Models
  """
  user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  title = models.CharField(max_length=25)
  desc = models.CharField(max_length=50)
  priority_levels = (
    ('HIGH', 'HIGH'),
    ('MEDIUM', 'MEDIUM'),
    ('LOW', 'LOW'))
  priority = models.CharField(choices = priority_levels, max_length=10)
  sch_date_time = models.DateTimeField(validators=[scheduled_date_validate])
  created_on = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name_plural = "Tasks"

  def __str__(self):
    return f'{self.user_id}: {self.title}'



