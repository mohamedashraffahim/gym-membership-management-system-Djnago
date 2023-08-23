from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from .models import Member
from datetime import datetime, timedelta

captainChoices = (
    ('Marwan', 'Marwan'),
    ('Hussein', 'Hussein'),
    ('Tarek', 'Tarek'),
    ('Diaa', 'Diaa'),
    ('Laila', 'Laila'),
    ('Shaher', 'Shaher')
)

durationChoices = (
    (30, '1 Month'),
    (60, '2 Months'),
    (90, '3 Months'),
    (120, '4 Months'),
)


class addMember(ModelForm):
    name = forms.CharField()
    age = forms.IntegerField()
    phone = forms.CharField()
    captain = forms.CharField(
        label='Captain', widget=forms.Select(choices=captainChoices))
    duration = forms.IntegerField(
        label='Duration', widget=forms.Select(choices=durationChoices))
    regDate = forms.DateField
    paid = forms.IntegerField()
    isAcive = True
    paymentCount = False
    # expDate = forms.DateTimeField
    # def __init__(self, *args, **kwargs):
    #     super(addMember, self).__init__(*args, **kwargs)
    #     if self.expDate == datetime.now:
    #         self.expDate = self.regDate + timedelta(days=self.duration)
    expDate = forms.DateField
    class Meta:
        model = Member
        fields = ['name', 'age', 'phone', 'captain',
                  'regDate', 'duration', 'paid']


class renewMember(ModelForm):
    duration = forms.IntegerField(
        label='Duration', widget=forms.Select(choices=durationChoices))
    paid = forms.IntegerField()
    isAcive = True

    class Meta:
        model = Member
        fields = ['duration', 'paid']
