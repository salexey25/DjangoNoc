from django import forms
from .models import Node, Equipment

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['name', 'location', 'contact', 'description']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['device', 'hostname', 'location']