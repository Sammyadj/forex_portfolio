from celery.app import shared_task
from celery.schedules import crontab
from forex_portfolio.celery import app
from portfolio.bot import run_bot
from portfolio.models import BotSettings


@shared_task
def run_bot_task():
    for bot_settings in BotSettings.objects.filter(is_active=True):
        run_bot(bot_settings.profile.id)


app.conf.beat_schedule = {
    'run-bot-every-minute': {
        'task': 'portfolio.tasks.run_bot_for_all_profiles',
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}
