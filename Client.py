from base64 import b64decode
from datetime import datetime
from json import loads, dumps
from random import randint, choice
from requests import get, post

from encrypt import encryption
from rubino import Rubino
from config import Config


class Client:

    dl_url , Dcsurl , getDcsurl , wsurl = "https://messengerX.iranlms.ir/GetFile.ashx", "https://messengerg2cX.iranlms.ir/", "https://getdcmess.iranlms.ir", "wss://msocket1.iranlms.ir:80"
    def __init__(self , auth:str, private_key):
        self.private = private_key

        if auth is len(auth) == 32:
            self.auth = auth


    def addContact(self, first_name, last_name, phone):
        return Client._create(self.auth, "addAddressBook", {"first_name": first_name, "last_name": last_name, "phone": phone})

    def addGroup(self, title, users_chat_id):
        return Client._create(self.auth, "addGroup", {"title": title, "member_guids": users_chat_id})

    def addChannel(self, title, channelType="Public", users_chat_id=None):
        return Client._create(self.auth, "addChannel", {"channel_type": channelType, "title": title, "member_guids": users_chat_id or []})

    def banMember(self, chat_id, member_id):
        return Client._create(self.auth, f"ban{Client._chatDetection(chat_id)}Member", {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id, "member_guid": member_id, "action": "Set"})

    def block(self, chat_id):
        return Client._create(self.auth, "setBlockUser", {"action": "Block", "user_guid": chat_id})


    @staticmethod
    def _create(auth, method, data, client=clients.web):
        return makeData(auth, encryption(encryption.changeAuthType(auth), private_key=Client.privateKey), method, dict(data))

    @staticmethod
    def _createTMP(method, data, tmp=None):
        return makeTmpData(method, dict(data), tmp=tmp, url=_getURL(DCsURL=Client.DCsURL, getDCsURL=Client.getDCsURL, dc_id=None))

    @staticmethod
    def _chatDetection(chat_id):
        return Tools.chatDetection(chat_id)

    def changeLink(self, chat_id):
        return Client._create(self.auth, f"set{Client._chatDetection(chat_id)}Link", {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id})

    def changePassword(self, hint, newPass, oldPass):
        return Client._create(self.auth, "changePassword", {"new_hint": hint, "new_password": newPass, "password": oldPass})

    def checkPassword(self, password):
        return Client._create(self.auth, "checkTwoStepPasscode", {"password": password}).get("data").get("is_vaild")


    def deleteContact(self, chat_id):
        return Client._create(self.auth, "deleteContact", {"user_guid": chat_id})

    def deleteMessages(self, chat_id, message_ids):
        return Client._create(self.auth, "deleteMessages", {"object_guid": chat_id, "message_ids": list(message_ids), "type": "Global"})
