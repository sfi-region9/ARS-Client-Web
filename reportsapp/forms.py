from django import forms
from django.forms import PasswordInput
from reportsapp import views as v
from reportsapp.apihandler import ApiHandler


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True)
    password = forms.CharField(widget=PasswordInput(), required=True)


class RegisterForm(forms.Form):
    name = forms.CharField(label="NAME First", max_length=100, required=True)
    username = forms.CharField(label="username", max_length=100, required=True)
    password = forms.CharField(widget=PasswordInput(), required=True)
    scc = forms.IntegerField(label="SCC#", required=True)
    email = forms.EmailField(label="Email", required=True)
    api = ApiHandler('https://api.sfiars.eu')
    vessels = [(i.vesselid, i.name.replace('_', ' ')) for i in api.readVessels()]
    vessel = forms.ChoiceField(choices=vessels, widget=forms.Select, required=True)


class ChangeVesselForm(forms.Form):
    api = ApiHandler('https://api.sfiars.eu')
    vessels = [(i.vesselid, i.name.replace('_', ' ')) for i in api.readVessels()]
    vessel = forms.ChoiceField(choices=vessels, widget=forms.Select, required=True)
