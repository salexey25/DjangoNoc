from django.db import models
from django.contrib.auth.models import User

class IPNetwork(models.Model):
    net_id = models.AutoField(primary_key=True)
    net_parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    net_prefix = models.CharField(max_length=18)  # Используйте GenericIPAddressField
    net_description = models.CharField(max_length=100)
    net_createdate = models.DateTimeField(auto_now_add=True)
    net_editdate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"IP Network {self.net_id}: {self.net_prefix}"

class DeletedNetwork(models.Model):
    net_prefix = models.CharField(max_length=18)
    net_description = models.TextField()
    net_createdate = models.DateTimeField()
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'old_db_deleted_networks'


class IPAddress(models.Model):
    ip_id = models.AutoField(primary_key=True)
    ip_parent_id = models.ForeignKey(IPNetwork, null=True, blank=True, on_delete=models.CASCADE)
    ip_add = models.CharField(max_length=18)  # Используйте GenericIPAddressField
    ip_description = models.CharField(max_length=100)
    ip_createdate = models.DateTimeField(auto_now_add=True)
    ip_editdate = models.DateTimeField(auto_now=True)
    ip_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)