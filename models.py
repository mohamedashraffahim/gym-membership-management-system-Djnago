from typing import Any
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


class Member(models.Model):
    mId = models.AutoField(primary_key=True)
    name = models.CharField('Name', max_length=100)
    age = models.IntegerField('Age', default=0)
    phone = models.CharField('Phone', max_length=12)
    captain = models.CharField('Captain', max_length=100)
    regDate = models.DateField('regDate', default=datetime.now)
    duration = models.IntegerField('Duration', default=30)
    expDate = models.DateField('expDate', default=datetime.now() + timedelta(days=30))
    paid = models.IntegerField('Paid', default=0)
    isActive = models.BooleanField('isActive', default=True)
    paymentCount = models.IntegerField('paymentCount', default=False)
