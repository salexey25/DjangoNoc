from django.db import models


class Rack(models.Model):
    nd_id = models.AutoField(primary_key=True)
    nd_city = models.CharField(max_length=100)
    nd_address = models.CharField(max_length=255)
    nd_name = models.CharField(max_length=100)
    nd_contact = models.CharField(max_length=255)
    nd_description = models.TextField()
    nd_rack_num = models.CharField(max_length=50, null=True, blank=True)
    nd_rack_unit = models.CharField(max_length=50, null=True, blank=True)
    nd_rack_type = models.CharField(max_length=50, null=True, blank=True)
    nd_parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rack {self.nd_id}"

class Device(models.Model):
    hw_id = models.AutoField(primary_key=True)
    hw_parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    hw_rack = models.ForeignKey('Rack', null=True, blank=True, on_delete=models.CASCADE)
    hw_ip = models.CharField(max_length=18)
    hw_vendor = models.CharField(max_length=100)
    hw_model = models.CharField(max_length=100)
    hw_hostname = models.CharField(max_length=255)
    hw_int_type = models.CharField(max_length=50)
    hw_int_num = models.PositiveIntegerField()

    def __str__(self):
        return f"Device {self.hw_id}"