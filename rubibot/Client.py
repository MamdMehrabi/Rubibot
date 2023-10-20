from base64 import b64decode
from datetime import datetime
from json import loads, dumps
from random import randint, choice
from connection import get, post

from encrypt import encryption
from rubino import Rubino
from config import Config


class Client:

    dl_url, DCsURL, getDCsURL, WSurl = "https://messengerX.iranlms.ir/GetFile.ashx", "https://messengerg2cX.iranlms.ir/", "https://getdcmess.iranlms.ir", "wss://msocket1.iranlms.ir:80"
    def __init__(self, auth, private_key):
        self.private = private_key

        if auth is len(auth) == 32:
            self.auth = auth
        elif auth is len(auth) != 32:
            raise Exception("Auth Invalid")

    def addContact(self, first_name, last_name, phone):
        return Client.create(self.auth, "addAddressBook", {"first_name": first_name, "last_name": last_name, "phone": phone})

    def addGroup(self, title, users_chat_id):
        return Client.create(self.auth, "addGroup", {"title": title, "member_guids": users_chat_id})

    def addChannel(self, title, channelType="Public", users_chat_id=None):
        return Client.create(self.auth, "addChannel", {"channel_type": channelType, "title": title, "member_guids": users_chat_id or []})

    def banMember(self, chat_id, member_id):
        return Client.create(self.auth, f"ban{Client._chatDetection(chat_id)}Member", {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id, "member_guid": member_id, "action": "Set"})

    def block(self, chat_id):
        return Client.create(self.auth, "setBlockUser", {"action": "Block", "user_guid": chat_id})


    @staticmethod
    def create(auth, method, data, client=Config.web):
        return Config.makeData(auth, encryption(encryption.changeAuthType(auth), private_key=Client.privateKey), method, dict(data))

    @staticmethod
    def createTMP(method, data, tmp=None):
        return Config.makeTmpData(method, dict(data), tmp=tmp, url=_getURL(DCsURL=Client.DCsURL, getDCsURL=Client.getDCsURL, dc_id=None))
    def changeLink(self, chat_id):
        return Client.create(self.auth, f"set{Client._chatDetection(chat_id)}Link", {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id})

    def changePassword(self, hint, newPass, oldPass):
        return Client.create(self.auth, "changePassword", {"new_hint": hint, "new_password": newPass, "password": oldPass})

    def checkPassword(self, password):
        return Client.create(self.auth, "checkTwoStepPasscode", {"password": password}).get("data").get("is_vaild")


    def deleteContact(self, chat_id):
        return Client.create(self.auth, "deleteContact", {"user_guid": chat_id})

    def deleteMessages(self, chat_id, message_ids):
        return Client.create(self.auth, "deleteMessages", {"object_guid": chat_id, "message_ids": list(message_ids), "type": "Global"})

    def getMe(self):
        return Client.getInfo(self)

    def getChats(self, start_id=None):
        return Client.create(self.auth, "getChats", {"start_id": start_id})

    def getMessages(self, chat_id, min_id, start_id=None):
        return Client.create(self.auth, "getMessagesInterval",
                           {"object_guid": chat_id, "middle_message_id": min_id, "start_id": start_id}).get("data").get(
            "messages")

    def getLastMessage(self, chat_id):
        return Client.getMessages(self, chat_id, Client.getInfo(self, chat_id)["chat"]["last_message"]["message_id"])[
            -1]  # it isn't a server method , is a shortcut

    def getInfoByUsername(self, username):
        return Client.create(self.auth, "getObjectByUsername", {"username": username.replace("@", "")})

    def getBlacklist(self, chat_id, start_id=None):
        return Client.create(self.auth, f"getBanned{Client._chatDetection(chat_id)}Members",
                           {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id, "start_id": start_id}).get("data")

    def getContactsUpdates(self):
        return Client.create(self.auth, "getContactsUpdates", {"state": round(datetime.today().timestamp()) - 200})

    def getMyBlacklist(self, start_id=None):
        return Client.create(self.auth, "getBlockedUsers", {"start_id": start_id})

    def getAbsObjects(self, chat_ids):
        return Client.create(self.auth, "getAbsObjects", {"object_guids": chat_ids})

    def getAdmins(self, chat_id, start_id=None):
        return Client.create(self.auth, f"get{Client._chatDetection(chat_id)}AdminMembers",
                           {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id, "start_id": start_id})

    def getAdminAccesses(self, chat_id, admin_guid):
        return Client.create(self.auth, f"get{Client._chatDetection(chat_id)}AdminAccessList",
                           {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id, "member_guid": admin_guid})

    def getMessagesInfo(self, chat_id, message_ids):
        return Client.create(self.auth, "getMessagesByID",
                           {"object_guid": chat_id, "message_ids": list(message_ids)}).get("data").get("messages")

    def getMembers(self, chat_id, search_text=None, start_id=None):
        return Client.create(self.auth, f"get{Client._chatDetection(chat_id)}AllMembers",
                           {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id, "search_text": search_text,
                            "start_id": start_id})

    def getInfo(self, chat_id=None):
        return Client.create(self.auth, f"get{'User' if chat_id is None else Client._chatDetection(chat_id)}Info",
                           {} if chat_id is None else {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id}).get(
            "data")

    def getLink(self, chat_id):
        return Client.create(self.auth, f"get{Client._chatDetection(chat_id)}Link",
                           {f"{Client._chatDetection(chat_id).lower()}_guid": chat_id}).get("data").get("join_link")

    def getPreviewByJoinLink(self, link):
        return Client.create(self.auth, f"{'group' if 'joing' in link else 'channel'}PreviewByJoinLink",
                           {"hash_link": link.split("/")[-1]})

    def getChatAds(self):
        return Client.create(self.auth, "getChatAds", {"state": round(datetime.today().timestamp()) - 200}).get("data")

    def getChatsUpdate(self):
        return Client.create(self.auth, "getChatsUpdates", {"state": round(datetime.today().timestamp()) - 200}).get(
            "data")

    def getChatUpdate(self, chat_id):
        return Client.create(self.auth, "getMessagesUpdates",
                           {"object_guid": chat_id, "state": round(datetime.today().timestamp()) - 200})

    def getGroupMentionList(self, group_guid, mention_text):
        return Client.create(self.auth, "getGroupMentionList", {"group_guid": group_guid, "search_mention": mention_text})

    def getGroupDefaultAccess(self, group_guid):
        return Client.create(self.auth, "getGroupDefaultAccess", {"group_guid": group_guid})

    def getMyStickerSet(self):
        return Client.create(self.auth, "getMyStickerSets", {})

    def getAvatars(self, chat_id):
        return Client.create(self.auth, "getAvatars", {"object_guid": chat_id})

    def getPollStatus(self, poll_id):
        return Client.create(self.auth, "getPollStatus", {"poll_id": str(poll_id)})

    def getPollOptionVoters(self, poll_id, option_index, start_id=None):
        return Client.create(self.auth, "getPollOptionVoters",
                           {"poll_id": poll_id, "selection_index": option_index, "start_id": start_id})

    def getPostByLink(self, link):
        return Client.create(self.auth, "getLinkFromAppUrl", {"app_url": link})["data"]["link"]["open_chat_data"]

    def getUserCommonGroups(self, chat_id):
        return Client.create(self.auth, "getCommonGroups", {"user_guid": chat_id})

    def getGroupOnlineMembersCount(self, chat_id):
        return Client.create(self.auth, "getGroupOnlineCount", {"group_guid": chat_id}).get("online_count")

    def getTwoPasscodeStatus(self):
        return Client.create(self.auth, "getTwoPasscodeStatus", {})

    def getPrivacySetting(self):
        return Client.create(self.auth, "getPrivacySetting", {})

    def getNotificationSetting(self):
        return Client.create(self.auth, "getNotificationSetting", {}).get("notification_setting")

    def getSuggestedFolders(self):
        return Client.create(self.auth, "getSuggestedFolders", {})

    def getFolders(self):
        return Client.create(self.auth, "getFolders", {}).get("folders")

    def getOwning(self, chat_id):
        return Client.create(self.auth, "getPendingObjectOwner", {"object_guid": chat_id})

    def getMySessions(self):
        return Client.create(self.auth, "getMySessions", {})

    def getContacts(self, start_id=None):
        return Client.create(self.auth, "getContacts", {"start_id": start_id})