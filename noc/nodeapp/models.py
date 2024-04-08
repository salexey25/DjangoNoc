from django.db import models

class Node(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    device = models.CharField(max_length=200)
    hostname = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    # Добавьте другие поля, такие как Port_id, если необходимо

    def __str__(self):
        return self.device
