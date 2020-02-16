from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from reportsapp.apihandler import *
from django.contrib import messages
from reportsapp.objects.utils import *
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm, ChangeVesselForm
from django.utils.translation import gettext as _

import json

global api, auth, vessels, default_by_id
api = ApiHandler('http://127.0.0.1:5555')
auth = AuthHandler('https://auth.sfiars.eu')
vessels = [(i.vesselid, i.name) for i in api.readVessels()]
e = {}

for i in api.readVessels():
    e[i.vesselid] = i.defaul


def index(request):
    lp = []
    lps = []
    dp = []
    dps = []
    d = api.getVesselByRegions()
    p = api.getReportsByDate()
    for i in d.keys():
        if d[i] > 0:
            lp.append('R' + i)
            lps.append(d[i])
    for i in p.keys():
        dp.append(str(i))
        dps.append(p[i])
    if not request.session.__contains__('username'):
        return render(request, '../templates/reportsapp/index.html',
                      {'session': False, 'lp': lp, 'lps': lps, 'dp': dp, 'dps': dps})
    else:
        api.synchronize_user(request.session)
        return render(request, '../templates/reportsapp/index.html',
                      {'session': request.session.__dict__['_session_cache'], 'lp': lp, 'lps': lps, 'dp': dp,
                       'dps': dps})


def ml(request):
    return render(request, '../templates/reportsapp/ml.html')


# Create your views here.
def login(request):
    if request.session.__contains__('username'):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_form = Login(form.cleaned_data['username'], form.cleaned_data['password'])
            req = auth.login(login_form, request.session)
            if req:
                messages.info(request, _("You are successfully login you're now ready to report!"))
                return HttpResponseRedirect('/' + request.LANGUAGE_CODE + "/")
            else:
                print("Error")
                messages.info(request, _(req))
                return HttpResponseRedirect('/' + request.LANGUAGE_CODE + '/login')

    login_form = LoginForm()
    return render(request, '../templates/reportsapp/login.html',
                  {'form': login_form, 'base': _('Log In'), 'submit': 'login'})


def register(request):
    if request.session.__contains__('username'):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            r = Register(form.cleaned_data['name'], form.cleaned_data['scc'], form.cleaned_data['username'],
                         form.cleaned_data['password'], form.cleaned_data['vessel'], form.cleaned_data['email'])
            req = auth.register(r)
            messages.info(request, _(req))
            if not req.__contains__('Error'):
                return HttpResponseRedirect('/login')
            else:
                return HttpResponseRedirect('/register')

    form = RegisterForm()
    return render(request, '../templates/reportsapp/login.html',
                  {'form': form, 'base': _('Register'), 'submit': 'register',
                   'session': request.session.__dict__['_session_cache']})


def profile(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        f = ChangeVesselForm(request.POST)
        if f.is_valid():
            fs = f.cleaned_data
            messages.info(request, _(api.switchvessel(request.session, fs['vessel'])))
            return HttpResponseRedirect('/')
    form = ChangeVesselForm()
    return render(request, '../templates/reportsapp/profile.html', {'form': form, 'session': request.session})


def logout(request):
    request.session.delete()
    messages.info(request, _('You logged out'))
    return HttpResponseRedirect('/')


def user(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/')
    l = ChangeVesselForm()
    return render(request, '../templates/reportsapp/user.html',
                  {'session': request.session.__dict__['_session_cache'], 'form': l})


@csrf_exempt
def change(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/')

    body = request.body.decode('utf8')
    data = json.loads(body)
    rapport = data['text']

    cf = rapport.split('\n')
    cf2 = e[request.session['vesselID']].split('\n')
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


@csrf_exempt
def communication(request):
    r = request.body.decode('utf8')
    print(r)
    jso = json.loads(r)
    report = jso['text']
    print(report)
    if report == "destroy":
        destroy(request.session)
        return HttpResponse('Redirect:main')
    if report == "profile":
        return HttpResponse('Redirect:profile')
    if report == "custom":
        return HttpResponse('Redirect:custom')
    return HttpResponse('False')


def destroy(session):
    api.destroy(session)
    auth.destroy(session)
    session.delete()
    return HttpResponseRedirect('/')


@csrf_exempt
def report(request):
    api.synchronize_user(request.session)
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/login')
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


def customization(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('/login')
    if not api.isco(request.session):
        return HttpResponseRedirect('/reports')
    return render(request, '../templates/reportsapp/customization.html',
                  {'session': request.session.__dict__['_session_cache']})


@csrf_exempt
def sendtemplate(request):
    r = request.body.decode('utf8')
    jso = json.loads(r)
    report = jso['text']
    print(report)
    api.update_template(request.session, report)
    return HttpResponse("s")


@csrf_exempt
def sendd(request):
    r = request.body.decode('utf8')
    jso = json.loads(r)
    report = jso['text']
    print(report)
    api.update_default(request.session, report)
    return HttpResponse("s")
