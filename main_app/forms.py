from django.forms import ModelForm
from .models import Agreement

class AgreementForm(ModelForm):
    class Meta:
        model = Agreement
        fields = ['agreement_num', 'unit_num', 'vin', 'license_num', 'mileage_out', 'condition', 'date', 'term', 'payment_freq']