from django.urls import path
from .views import AccountHistoryView, BotSettingsView

urlpatterns = [
    path('account-history/<int:profile_id>/', AccountHistoryView.as_view(), name='account-history'),
    path('bot-settings/<int:profile_id>/', BotSettingsView.as_view(), name='bot-settings'),
]