from requests import get, post
from encrypt import encryption
from json import dumps, loads, decoder
from exception import NotRegistred, InvalidAuth, InvalidInput, TooRequests
from config import Config
class connection:

    def POST(self, json: dict, method, url: str = None, platform="web.rubika.ir", enc: encryption = None, isEncrypted: bool = True) -> dict:
        while 1:
            try:
                response = post(url=url, json=json, headers={
                    'Origin': 'https://' + platform,
                    'Referer': f'https://{platform}/',
                    'Host': url.replace("https://", "").replace("/", ""),
                    'User-Agent': Config.USER_AGENT
                }).text
                response = loads(str(enc.decrypt(loads(response).get("data_enc")))) if "data_enc" in loads(
                    response).keys() and isEncrypted else loads(response)
                if "status" in response.keys() and response.get("status") != "OK":
                    if response.get("status_det") == "NOT_REGISTERED":
                        raise NotRegistred(
                            "the auth is incorrect. please sure about your account's health then login again.")
                    elif response.get("status_det") == "INVALID_INPUT":
                        raise InvalidInput(
                            f"the inserted argument(s) is invaild in the {platform}/{method}. if you're sure about your argument(s), please report this message.")
                    elif response.get("status_det") == "TOO_REQUESTS":
                        raise TooRequests(f"the {platform}/{method} method has been limited. please try again later.")
                    elif response.get("status_det") == 'INVALID_AUTH':
                        raise InvalidAuth(
                            f"the inserted argument(s) in {platform}/{method} is vaild but is not related to other argument(s) or maybe for other reasons, anyway now this method can't run on server. please don't enter fake argument(s) and fix anything can return this exception")
                else:
                    return response
            except decoder.JSONDecodeError:
                ...
            except ConnectionError:
                url = Config.getURL(dc_id=64)