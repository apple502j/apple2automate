import json

def clearAllWarnings():
    try:
        with open("blocklist.json", "r") as jf:
            warndata=json.load(jf)
            warndata["warning"] = [""]
            jf.seek(0)
        with open("blocklist.json", "w") as jf:
            json.dump(warndata, jf)
    except json.decoder.JSONDecodeError:
        pass

def setWarnType(name,warntype,remove=False):
    if warntype not in ['warning','alert','block','no']:
        return
    else:
        try:
            with open("blocklist.json", "r") as jf:
                warndata=json.loads(jf.read())
            if name not in warndata[warntype] and (not remove):
                warndata[warntype].append(name)
                if warntype == 'alert' and name in warndata["warning"]:
                    warndata["warning"].remove(name)
                if warntype == 'block' and name in warndata["warning"]:
                    warndata["warning"].remove(name)
                if warntype == 'block' and name in warndata["alert"]:
                    warndata["alert"].remove(name)
            if name in warndata[warntype] and remove:
                warndata[warntype].remove(name)
            with open("blocklist.json", "w") as jf:
                json.dump(warndata,jf)
        except json.decoder.JSONDecodeError:
            pass

class WarnType:
    block = 3
    alert = 2
    warning = 1
    no = 0

def getWarnType(name):
    with open("blocklist.json","r") as jf:
        try:
            warndata=json.loads(jf.read())
            if name in warndata["block"]:
                return WarnType.block
            elif name in warndata["alert"]:
                return WarnType.alert
            elif name in warndata["warning"]:
                return WarnType.warning
            else:
                return WarnType.no
        except json.decoder.JSONDecodeError:
            return WarnType.no

isBlocked=lambda n:getWarnType(n)==WarnType.block
