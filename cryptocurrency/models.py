from djongo import models
from django.utils.timezone import now

class Coin(models.Model):
    name = models.CharField(max_length=3 , primary_key= True)

class Technical_Analysis(models.Model):
    class Type(models.TextChoices):
        SMA = 'SMA', "SMA"
        EMA = 'EMA' , "EMA"
    type = models.CharField(max_length=3,choices=Type.choices)


class Event(models.Model):
    current_currency = models.ForeignKey(Coin ,on_delete=models.CASCADE, related_name="current_currency")
    base_currency = models.ForeignKey(Coin,on_delete=models.CASCADE, related_name="base_currency")
    date = models.DateTimeField(default=now)
    type = models.ForeignKey(Technical_Analysis,on_delete=models.CASCADE)
    type_value = models.CharField(max_length=48)
    is_signalable = models.BooleanField(default=False)