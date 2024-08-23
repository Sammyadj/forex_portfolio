from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import AccountHistory, BotSettings
from .serializers import AccountHistorySerializer, BotSettingsSerializer


class AccountHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):
        history = AccountHistory.objects.filter(profile_id=profile_id).order_by('-timestamp')[:100]
        serializer = AccountHistorySerializer(history, many=True)
        return Response(serializer.data)


class BotSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):
        bot_settings, created = BotSettings.objects.get_or_create(profile_id=profile_id)
        serializer = BotSettingsSerializer(bot_settings)
        return Response(serializer.data)

    def post(self, request, profile_id):
        bot_settings, created = BotSettings.objects.get_or_create(profile_id=profile_id)
        data = request.data
        action = data.get('action')

        # Handle the start/stop actions
        if action == 'start':
            bot_settings.is_active = True
        elif action == 'stop':
            bot_settings.is_active = False

        # Save the updated bot settings
        bot_settings.save()
        serializer = BotSettingsSerializer(bot_settings)
        return Response(serializer.data)

# class BotSettingsView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, profile_id):
#         bot_settings, created = BotSettings.objects.get_or_create(profile_id=profile_id)
#         serializer = BotSettingsSerializer(bot_settings)
#         return Response(serializer.data)
#
#     def post(self, request, profile_id):
#         bot_settings, created = BotSettings.objects.get_or_create(profile_id=profile_id)
#         data = request.data
#         action = data.get('action')
#
#         if action == 'start':
#             bot_settings.is_active = True
#         elif action == 'stop':
#             bot_settings.is_active = False
#
#         bot_settings.instrument = data.get('instrument', bot_settings.instrument)
#         bot_settings.short_ma_period = data.get('short_ma_period', bot_settings.short_ma_period)
#         bot_settings.long_ma_period = data.get('long_ma_period', bot_settings.long_ma_period)
#         bot_settings.granularity = data.get('granularity', bot_settings.granularity)
#
#         bot_settings.save()
#         serializer = BotSettingsSerializer(bot_settings)
#         return Response(serializer.data)
