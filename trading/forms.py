from django import forms
from .models import Trade, Instrument


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['instrument', 'volume']

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.all()
