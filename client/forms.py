from django import forms
from .models import Reserva
from django.utils import timezone
import datetime
from .models import Cliente
import calendar


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'sexo']


class ReservaForm(forms.ModelForm):
    dia = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = Reserva
        fields = ['dia']
        
    def clean_dia(self):
        dia = self.cleaned_data.get('dia')
        fecha_actual = timezone.now().date()
        fecha_limite = fecha_actual + datetime.timedelta(days=1)

        if dia < fecha_limite:
            raise forms.ValidationError("Debes realizar la reserva con al menos un día de anticipación.")
        if dia < fecha_actual:
            raise forms.ValidationError("No puedes reservar una fecha pasada.")

        if dia.weekday() == calendar.SUNDAY:
            raise forms.ValidationError("Los domingos no se pueden reservar.")

    
        agenda = self.cleaned_data.get('agenda')
        if Reserva.objects.filter(agenda=agenda, dia=dia).exists():
            raise forms.ValidationError("La fecha ya está reservada.")

        return dia

