from django.forms import ModelForm
from .models import Agreement

class AgreementForm(ModelForm):
    class Meta:
        model = Agreement
        fields = '__all__'