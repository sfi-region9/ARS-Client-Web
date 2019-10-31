class Register:
    def __init__(self, name, scc, username, password, vessel, email):
        self.name = name
        self.scc = scc
        self.username = username
        self.password = password
        self.vessel = vessel
        self.email = email


class Vessel:
    def __init__(self, name, vesselid, coid, template, defaul):
        self.name = name
        self.vesselid = vesselid
        self.coid = coid
        self.template = template
        self.defaul = defaul


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class User:
    def __init__(self, name, vesselid, scc, report, uuid):
        self.name = name
        self.vesselid = vesselid
        self.scc = scc
        self.report = report
        self.uuid = uuid


class StorageHandler:
    def __init__(self, session):
        self.session = session
        self.username = session['username']
        self.name = session['name']
        self.vesselid = session['vesselid']
        self.scc = session['scc']
        self.uuid = session['uuid']
        self.messengerid = session['messengerid']
        if session.__contains__('report'):
            self.report = session['report']
        else:
            self.report = ''

    def constructUser(self):
        return User(self.name, self.vesselid, self.scc, self.report, self.uuid)
