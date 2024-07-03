from django.urls import path
from .views import *

app_name = 'trading'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('trade/open/', open_trade, name='open_trade'),
    path('trade/close/<int:trade_id>/', close_trade, name='close_trade'),
]


