from django.core.management.base import BaseCommand
from portfolio.bot import run_bot
from portfolio.models import BotSettings


class Command(BaseCommand):
    help = 'Run the trading bot manually'

    def handle(self, *args, **kwargs):
        # You could add logic here to run the bot for specific profiles or all active ones
        for bot_settings in BotSettings.objects.filter(is_active=True):
            run_bot(bot_settings.profile.id)
        self.stdout.write(self.style.SUCCESS('Bot has been run successfully'))