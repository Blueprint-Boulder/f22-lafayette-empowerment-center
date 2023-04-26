from django.db import models

class Donations(models.Model):
    transaction_id = models.CharField(max_length=20)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amt = models.FloatField()
    custom_message = models.CharField(max_length=250)
    program = models.CharField(max_length=200)
