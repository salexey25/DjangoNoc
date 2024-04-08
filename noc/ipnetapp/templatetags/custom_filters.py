from django import template

register = template.Library()

@register.filter
def sort_custom(networks):
    def custom_sort(network):
        ip, label = network.split(" - ")
        third_octet = int(ip.split(".")[2])
        return third_octet

    return sorted(networks, key=custom_sort)