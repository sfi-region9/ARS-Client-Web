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
            v = Vessel(name=i['name'], vesselid=i['vesselID'], coid=i['coID'], template=i['template'],
                       defaul=i['defaultReport'])
            r.append(v)
        return r

    def synchronize_user(self, session):
        if not session.__contains__('username'):
            return "Error you're not logged"
        s = StorageHandler(session)
        response = requests.post(self.url + "/synchronize_user", data=json.dumps(s.constructUser().__dict__))
        df = response.content.decode('utf8')
        jso = json.loads(df)
        session['name'] = jso['name']
        session['scc'] = jso['scc']
        session['vesselID'] = jso['vesselID']
        session['report'] = jso['report']
        session['uuid'] = jso['uuid']

        return "Session successfully updated"

    def switchvessel(self, session, newvessel):
        if not session.__contains__('username'):
            return "Error you're not logged"
        s = StorageHandler(session)
        u = s.constructUser()
        u.vesselid = newvessel
        requests.post(self.url + "/switch_vessel", data=json.dumps(u.__dict__))
        return "You changed to the : " + str(newvessel)

    def isco(self, session):
        if not session.__contains__('username'):
            return "Error you're not logged"
        s = StorageHandler(session)
        dic = {"vesselID": s.vesselID, "coID": s.messengerid}
        payload = dic
        response = requests.post(self.url + "/check_co", data=json.dumps(payload))
        return response.content.decode('utf8')

    def sendreport(self, session, report):
        if not session.__contains__('username'):
            return "Error you're not logged"
        s = StorageHandler(session)
        s.report = report
        response = requests.post(self.url + "/submit", data=json.dumps(s.constructUser().__dict__))
        return response.content.decode("utf8")

    def destroy(self, session):
        s = StorageHandler(session)
        response = requests.post(self.url + "/destroy_user", data=json.dumps(s.constructUser().__dict__))
        return response.content.decode('utf8')

    def update_template(self, session, template):
        s = StorageHandler(session)
        ss = {'vesselID': s.vesselID, 'coID': s.messengerid, 'template': template}
        response = requests.post(self.url + "/update_template", data=json.dumps(ss))
        return "True"

    def update_default(self, session, default):
        s = StorageHandler(session)
        ss = {'vesselID': s.vesselID, 'coID': s.messengerid, 'text': default}
        response = requests.post(self.url + "/update_name", data=json.dumps(ss))

    def getVesselByRegions(self):
        return json.loads(requests.get(self.url + "/vessel_by_regions").content.decode('utf8'))

    def getReportsByDate(self):
        return json.loads(requests.get(self.url + "/reports_by_date").content.decode('utf8'))


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
            session['vesselID'] = sdf[2]
            session['name'] = sdf[3]
            session['messengerid'] = sdf[4]
            session['uuid'] = sdf[5]
            session.modified = True
            return True
        else:
            return s

    def register(self, user):
        payload = modelToDic(user)
        dic2 = {'name': payload['name'], 'username': payload['username'], 'password': payload['password'],
                'vessel': payload['vessel'], 'email': payload['email'], 'scc': "SCC#" + str(payload['scc'])}
        data = requests.post(url=self.url + "/register", data=None, json=dic2)
        s = data.content.decode('utf8')
        return s

    def destroy(self, session):
        s = StorageHandler(session)
        response = requests.post(self.url + "/destroy_user", data=json.dumps(s.constructUser().__dict__))
        return response.content.decode('utf8')


def modelToDic(model):
    dic = vars(model)
    return dic
