from django.core.management.base import BaseCommand
from app.models import Tasks
import datetime
import pytz
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
  help = 'Send notifications fors tasks that are close to \
          scheduled date/time'
  
  def handle(self, *args, **options):
    tasks = Tasks.objects.all()
    now = datetime.datetime.now()
    for i in tasks:
      if i.sch_date_time.date() == now.date():
        remaining = i.sch_date_time - pytz.timezone("Asia/Kolkata").\
                                      localize(now)
        rem_hours = remaining.seconds/(60*60)
        if rem_hours <= 1:
          subject = "ToDo App reminder."
          message = f"Hi {i.user_id.username}, \n \
                      Below scheduled task will begin within an hour. \n  \
                      - TASK: {i.title} \n  \
                      - DESC: {i.desc} \n \
                      - Scheduled date: {i.sch_date_time.date()} \n \
                      - Scheduled time: {i.sch_date_time.time()}"
                       
          email_from = settings.EMAIL_HOST_USER
          recipient_list = [i.user_id.email,]
          send_mail(subject, message, email_from, recipient_list)
                      
          self.stdout.write("########################################")
          self.stdout.write("Notification has been sent successfully for:")
          self.stdout.write(f'TASK: {i.title}')
          self.stdout.write(f'DESC: {i.desc}')
          self.stdout.write(f'Email: {i.user_id.email}')
          self.stdout.write("########################################")
