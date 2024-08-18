from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import APIRootView, InstrumentListView, CurrentPriceView, CandleDataView, TradeViewSet


router = DefaultRouter()
router.register(r'trades', TradeViewSet)

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('instruments/', InstrumentListView.as_view(), name='instrument-list'),
    path('instruments/<str:instrument_name>/', InstrumentListView.as_view(), name='instrument-detail'),
    path('pricing/<str:instrument_name>/', CurrentPriceView.as_view(), name='current-price'),
    path('candles/<str:instrument_name>/', CandleDataView.as_view(), name='candle-data'),
    path('', include(router.urls))
]
