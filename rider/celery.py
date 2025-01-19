# import os
# from celery import Celery
# from celery.schedules import crontab

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rider.settings')

# app = Celery('rider')

# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     "mark_absent": {
#         "task": "mark_absent_for_un_logged_users",
#         "schedule": crontab(minute=1, hour=23),
#     },
#     "auto_check_out": {
#         "task": "auto_check_out",
#         "schedule": crontab(minute=1, hour=22),
#     },
#     "calculate_monthly_balance": {
#         "task": "calculate_monthly_balance",
#         "schedule": crontab(day_of_month=1),
#     },
#     "calculate_yearly_balance": {
#         "task": "calculate_yearly_balance",
#         "schedule": crontab(day_of_month=1),
#     },
# }
