from django import forms
from django.forms import PasswordInput
from reportsapp import views as v
from reportsapp.apihandler import ApiHandler


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=PasswordInput())


class RegisterForm(forms.Form):
    name = forms.CharField(label="NAME First", max_length=100)
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(widget=PasswordInput())
    scc = forms.IntegerField(label="SCC#")
    email = forms.EmailField(label="Email")
    api = ApiHandler('https://ars.nwa2coco.fr')
    vessels = [(i.vesselid, i.name.replace('_', ' ')) for i in api.readVessels()]
    vessel = forms.ChoiceField(choices=vessels)


class ChangeVesselForm(forms.Form):
    api = ApiHandler('https://ars.nwa2coco.fr')
    vessels = [(i.vesselid, i.name.replace('_', ' ')) for i in api.readVessels()]
    vessel = forms.ChoiceField(choices=vessels)
