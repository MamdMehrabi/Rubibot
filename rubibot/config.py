from connection import get, post
from encrypt import encryption
from connection import connection
from json import dumps, loads
from random import choice, sample
class Config:

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"

    pwa = {
        "app_name": "Main",
        "app_version": "1.2.1",
        "platform": "PWA",
        "package": "m.rubika.ir",
        "lang_code": "fa"
    }
    web = {
        "app_name": "Main",
        "app_version": "4.3.3",
        "platform": "Web",
        "package": "web.rubika.ir",
        "lang_code": "fa"
    }
    android = {
        "app_name": "Main",
        "app_version": "2.9.8",
        "platform": "Android",
        "package": "app.rbmain.a",
        "lang_code": "fa"
    }

    def getURL(self, key="default_api_urls", DCsURL: str="https://messangerg2cX.iranlms.ir/", getDCsURL: str="https://getdcmess.iranlms.ir", dc_id:int=None):
        while 1:
            res = post(json={"api_version": 4, "client": Config.pwa, "method": "getDCs"}, url=getDCsURL).json().get("data").get(key)
            return DCsURL.replace('X', dc_id) if dc_id is not None else choice(list(res))

    def makeData(auth: str, enc: encryption, method: str, data: dict, client: dict = Config.web, url: str = None) -> dict:
        url = url or Config.getURL()
        outerJson = {
            "api_version": "6",
            "auth": auth,
            "data_enc": {
                "method": method,
                "input": data,
                "client": client
            }
        }
        outerJson["data_enc"] = enc.encrypt(dumps(outerJson["data_enc"]))
        outerJson["sign"] = enc.makeSignFromData(outerJson["data_enc"])
        return connection.POST(outerJson, url=url, platform=client.get('package'), method=method, enc=enc)

    def makeTmpData(method: str, data: dict, url: str = None, tmp: str = None) -> dict:
        url, tmp = url or Config.getURL(), encryption.changeAuthType(tmp or tmpGeneration())
        enc = encryption(tmp)
        outerJson = {
            "api_version": "6",
            "tmp_session": tmp,
            "data_enc": enc.encrypt(dumps({
                "method": method,
                "input": data,
                "client": Config.web
            }))
        }

        resp = connection.POST(outerJson, method, url=url, platform=Config.web.get("package"), enc=enc)
        resp['tmp'] = tmp
        return resp