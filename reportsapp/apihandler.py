import requests
import json
from reportsapp.objects.utils import *


class ApiHandler:
    def __init__(self, url):
        self.url = url

    def readVessels(self):
        response = requests.get(self.url + '/allvessels')
        data = response.json()
        r = []
        for i in data:
            v = Vessel(name=i['name'], vesselid=i['vesselid'], coid=i['coid'], template=i['template'],
                       defaul=i['defaul'])
            r.append(v)
        return r

    def syncronize_user(self, session):
        if not session.__contains__('username'):
            return "Error you're not logged"
        s = StorageHandler(session)
        response = requests.post(self.url + "/syncronize_user", data=json.dumps(s.constructUser().__dict__))
        jso = json.loads(response.content.decode('utf8'))
        session['name'] = jso['name']
        session['scc'] = jso['scc']
        session['vesselid'] = jso['vesselid']
        session['report'] = jso['report']
        session['uuid'] = jso['uuid']
        return "Session successfully updated"

    def isco(self, session):
        if not session.__contains__('username'):
            return "Error you're not logged"
        s = StorageHandler(session)
        dic = {"vesselid": s.vesselid, "coid": s.messengerid}
        payload = dic
        response = requests.post(self.url + "/check_co", data=json.dumps(payload))
        return response.content.decode('utf8')

    def sendreport(self, session, report):
        if not session.__contains__('username'):
            return "Error you're not logged"
        s = StorageHandler(session)
        s.report = report
        reponse = requests.post(self.url + "/submit", data=json.dumps(s.constructUser().__dict__))
        return reponse.content.decode("utf8")


class AuthHandler:
    def __init__(self, url):
        self.url = url

    def login(self, user, session):
        payload = modelToDic(user)
        dic = {'username': payload['username'], 'password': payload['password']}
        data = requests.post(url=self.url + "/login", data=None, json=dic)
        s = data.content.decode('utf8')
        if s.__contains__("}_}"):
            sdf = s.split('}_}')
            session['username'] = sdf[0]
            session['scc'] = sdf[1]
            session['vesselid'] = sdf[2]
            session['name'] = sdf[3]
            session['messengerid'] = sdf[4]
            session['uuid'] = sdf[5]
            session.modified = True
            return True
        else:
            return False

    def register(self, user):
        payload = modelToDic(user)
        dic2 = {'name': payload['name'], 'username': payload['username'], 'password': payload['password'],
                'vessel': payload['vessel'], 'email': payload['email'], 'scc': "SCC#" + payload['scc']}
        data = requests.post(url=self.url + "/register", data=None, json=dic2)
        s = data.content.decode('utf8')
        return s


def modelToDic(model):
    dic = vars(model)
    return dic
