from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Trade, Instrument, Strategy
from .forms import TradeForm
from django.http import JsonResponse

from .api_utils import get_account_instruments


@login_required
def dashboard(request):

    trades = Trade.objects.filter(profile__user=request.user, is_open=True)
    context = {
        'trades': trades,
        'balance': request.user.profile.balance  # Ensure the user has a profile with a balance
    }
    return render(request, 'trading/dashboard.html', context)


def open_trade(request):
    # Assuming there's form handling here
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            new_trade = form.save(commit=False)
            new_trade.profile = request.user.profile
            new_trade.save()
            return redirect('trading:dashboard')
    else:
        form = TradeForm()
    return render(request, 'trading/open_trade.html', {'form': form})


def close_trade(request, trade_id):
    trade = get_object_or_404(Trade, pk=trade_id)
    if request.method == 'POST':
        # Assuming the trade closing logic here
        trade.close_trade()
        return redirect('trading:dashboard')
    return render(request, 'trading/close_trade.html', {'trade': trade})


def test_api(request):
    data = get_account_instruments()
    return JsonResponse(data)


def list_instruments(request):
    instruments = Instrument.objects.all()
    return render(request, 'trading/list_instruments.html', {'instruments': instruments})
