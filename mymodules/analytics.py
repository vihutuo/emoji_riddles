import requests
import pendulum
import threading
import time
import hashlib


def GetCurrentDateTime(tmz="Asia/Kolkata"):
    now = pendulum.now(tmz)
    return now


class Analytics:
    def __init__(self, appid: int,salt,pepper_code,analytics_domain,this_url):
        self.appid = appid
        self.timeout = 10

        self.session_id = 0
        self.match_no = 0
        self.match_id = 0
        self.domain = analytics_domain
        self.url =  this_url
        self.salt = salt
        self.pepper_code = pepper_code
        self.pepper = 0

    def getpepper(self):
        exec(self.pepper_code)
        return self.pepper

    def getcurry(self):
        hash = hashlib.new('sha256')
        hash.update((self.salt + str(self.getpepper())).encode())
        return hash.hexdigest()

    def getheaders(self):
        headers = {
            'appid': str(self.appid),
            "food": self.getcurry()
            #"pepper": str(self.pepper)

        }
        return headers

    def StartSession(self, ip: str = "", user_agent: str = "", player_name: str = "", platform: str = "",
                      flet_session_id: str = ""):
        URL = f"{self.domain}/apps/{self.appid}/sessions/"
        now = GetCurrentDateTime().to_iso8601_string()
        data = {'ip': ip, "start_time": now, "user_agent": user_agent,
                "player_name": player_name, "platform": platform, "url": self.url, "flet_session_id": flet_session_id}
        h = self.getheaders()

        def Go():
            try:
                response = requests.post(url=URL, json=data, timeout=self.timeout, headers=h)
                if response.status_code == 200:
                    data_r = response.json()
                    self.session_id = data_r["id"]
                else:
                    return False
            except Exception as error:
                print(error)
                return False

        threading.Timer(0, Go).start()

    def UpdateSession(self, player_name: str):
        if self.session_id <= 0:
            return False
        URL = f"{self.domain}/sessions/{self.session_id}"
        data = {"player_name": player_name}
        h = self.getheaders()

        def Go():
            try:
                response = requests.patch(url=URL, json=data, timeout=self.timeout, headers=h)
            except Exception as error:
                print(error)
                return False

        threading.Timer(0, Go).start()

    def StartMatch(self, initial_value: str):

        def Go():
            try:
                for i in range(5):
                    if self.session_id <= 0:
                        print("Waiting as session id is 0")
                        time.sleep(3)
                    else:
                        break

                if self.session_id <= 0:
                   return False

                # nonlocal URL
                now = GetCurrentDateTime().to_iso8601_string()
                self.match_no += 1

                data = {"start_time": now, "match_no": str(self.match_no),
                        "score": "0", "initial_value": initial_value}
                URL = f"{self.domain}/sessions/{self.session_id}/matches/"
                h = self.getheaders()
                response = requests.post(url=URL, json=data, timeout=self.timeout, headers=h)
                data_r = response.json()
                self.match_id = data_r["id"]
            except Exception as error:
                print("Start Match Error", error)
                return False

        threading.Timer(0, Go).start()

    def UpdateMatch(self, score: int):
        if self.session_id <= 0:
            return False
        URL = f"{self.domain}/matches/{self.match_id}"
        now = GetCurrentDateTime().to_iso8601_string()
        self.match_no += 1

        data = {"end_time": now, "score": score}
        h = self.getheaders()

        def Go():
            try:
                response = requests.patch(url=URL, json=data, timeout=self.timeout, headers=h)
            except Exception as error:
                print("End Match Error", error)
                return False

        threading.Timer(0, Go).start()

    def SaveKeyValue(self, key_name: str, value_int: int = 0, value_str: str = ""):
        URL = f"{self.domain}/matches/{self.match_id}/keyvalues/"
        now = GetCurrentDateTime().to_iso8601_string()
        data = {"key_name": key_name, "insert_time": now, "value_int": value_int,
                "value_str": value_str, }
        h = self.getheaders()

        def Go():
            try:
                response = requests.post(url=URL, json=data, timeout=self.timeout, headers=h)

            except Exception as error:
                print(error)
                return False

        threading.Timer(0, Go).start()

    def GetApps(self):
        URL = f"{self.domain}/apps/"
        PARAMS = {'skip': 0, 'limit': 100}
        h = self.getheaders()
        response = requests.get(url=URL, params=PARAMS, headers=h, timeout=self.timeout)
        data = response.json()
        return data
    def get_high_scores(self,limit:int = 10, min_score: int = 0):
        URL = f"{self.domain}/high_scores/"
        PARAMS = {'appid': self.appid, 'min_score': min_score, 'limit': limit}
        h = self.getheaders()
        response = requests.get(url=URL, params=PARAMS, headers=h, timeout=self.timeout)
        try:
            data = response.json()
            return data
        except Exception as error:
            print(error)
            return False
