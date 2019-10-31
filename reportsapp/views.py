from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from reportsapp.apihandler import *
from django.contrib import messages
from reportsapp.objects.utils import *
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm, ChangeVesselForm
import json

global api, auth, vessels, default_by_id
api = ApiHandler('https://ars.nwa2coco.fr')
auth = AuthHandler('https://auth.nwa2coco.fr')
vessels = [(i.vesselid, i.name) for i in api.readVessels()]
e = {}

for i in api.readVessels():
    e[i.vesselid] = i.defaul


def index(request):
    if not request.session.__contains__('username'):
        return render(request, '../templates/reportsapp/index.html',
                      {'session': False})
    else:
        api.syncronize_user(request.session)
        return render(request, '../templates/reportsapp/index.html',
                      {'session': request.session.__dict__['_session_cache']})


# Create your views here.
def login(request):
    if request.session.__contains__('username'):
        return HttpResponseRedirect('/reports/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            l = Login(form.cleaned_data['username'], form.cleaned_data['password'])
            req = auth.login(l, request.session)
            if req:
                return HttpResponseRedirect('/reports/')
            else:
                messages.info(request, req)

    l = LoginForm()
    return render(request, '../templates/reportsapp/login.html', {'form': l, 'base': 'Log In', 'submit': 'login'})


def register(request):
    if request.session.__contains__('username'):
        return HttpResponseRedirect('/reports/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            r = Register(form.cleaned_data['name'], form.cleaned_data['scc'], form.cleaned_data['username'],
                         form.cleaned_data['password'], form.cleaned_data['vessel'], form.cleaned_data['email'])
            req = auth.register(r)
            messages.info(request, req)
            return HttpResponseRedirect('/reports/login')
    form = RegisterForm()
    return render(request, '../templates/reportsapp/login.html',
                  {'form': form, 'base': 'Register', 'submit': 'register'})


def logout(request):
    request.session.delete()
    messages.info(request, "You log out")
    return HttpResponseRedirect('/reports/')


def user(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/reports/')
    l = ChangeVesselForm()
    return render(request, '../templates/reportsapp/user.html',
                  {'session': request.session.__dict__['_session_cache'], 'form': l})


@csrf_exempt
def change(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/reports/')

    body = request.body.decode('utf8')
    data = json.loads(body)
    rapport = data['text']

    cf = rapport.split('\n')
    cf2 = e[request.session['vesselid']].split('\n')
    cf3 = []
    for i in cf2:
        if not i.startswith('#'):
            cf3.append(i)

    i = 0
    for cs in cf:
        if not cs.startswith(cf3[i]):
            if not cf3[i].startswith('#'):
                return HttpResponseServerError('False')
        i += 1
        if i > len(cf3) - 1:
            break
    return HttpResponse('True')


def communication(request):
    return HttpResponse('False')


@csrf_exempt
def report(request):
    api.syncronize_user(request.session)
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/login/')

    re = request.session['report']
    res = re.split('\n')
    ress = []
    for i in res:
        if not i.startswith("#"):
            ress.append(i)
        else:
            ress.append(i.replace('#', ' '))
    default_value = '\n'.join(ress)
    return render(request, '../templates/reportsapp/reports.html',
                  {'session': request.session.__dict__['_session_cache'], 'default_value': default_value,
                   'isco': api.isco(request.session)})


@csrf_exempt
def sendreport(request):
    r = request.body.decode('utf8')
    jso = json.loads(r)
    report = jso['text']
    s = api.sendreport(request.session, report)
    return HttpResponse(s)
