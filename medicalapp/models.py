from django.db import models

class customer(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=10)  


class Medicine(models.Model):
    user = models.ForeignKey(customer, on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']