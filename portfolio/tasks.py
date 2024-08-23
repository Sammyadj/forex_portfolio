from celery.app import shared_task
from celery.schedules import crontab
from accounts.models import Profile
from forex_portfolio.celery import app
from portfolio.bot_portfolio import PortfolioBot


@shared_task
def run_portfolio_bot(profile_id):
    try:
        profile = Profile.objects.get(id=profile_id)
        bot = PortfolioBot(profile)
        bot.run()
    except Profile.DoesNotExist:
        print(f"Profile with id {profile_id} does not exist.")
    except Exception as e:
        print(f"Error running portfolio bot: {str(e)}")


@shared_task
def run_bot_for_all_profiles():
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile:
            run_portfolio_bot.delay(profile.id)


app.conf.beat_schedule = {
    'run-bot-for-all-profiles-every-minute': {
        'task': 'portfolio.tasks.run_bot_for_all_profiles',
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}


