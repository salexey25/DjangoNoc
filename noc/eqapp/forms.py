from django import forms
from .models import Device, Rack

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['hw_vendor', 'hw_model', 'hw_hostname', 'hw_int_type', 'hw_int_num']

class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['nd_rack_num', 'nd_rack_unit', 'nd_rack_type']

class NodeForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['nd_city','nd_address', 'nd_name', 'nd_contact', 'nd_description']
