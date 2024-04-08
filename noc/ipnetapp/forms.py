from django import forms
from .models import IPNetwork

class IPNetworkForm(forms.ModelForm):
    class Meta:
        model = IPNetwork
        fields = ['net_prefix', 'net_description']

class NetworkDivisionForm(forms.Form):

    network_choices = [(network.net_id, network.net_prefix) for network in IPNetwork.objects.all()]
    network = forms.ChoiceField(choices=network_choices)
#    action = forms.ChoiceField(choices=[('subnets', 'Divide into subnets'), ('hosts', 'Create a list of IP addresses')])
    subnet_bits = forms.ChoiceField(choices=[(i, i) for i in range(23, 33)], required=False)
    # CHOICES = [
    #     ('subnets', 'Разделить на подсети'),
    #     ('ip_list', 'Разделить на список IP-адресов'),
    # ]
    #
    # division_choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
