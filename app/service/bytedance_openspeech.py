import requests


class BytedanceOpenspeechClientError(Exception):

    def __init__(self, message: str, status_code: int, service_code: str | None):
        self.message = message
        self.status_code = status_code
        self.service_code = service_code
        super().__init__(self.message)

    def __str__(self):
        return f"BytedanceOpenspeechClientError: {self.message} -- {self.status_code} -- {self.service_code}"


class BytedanceOpenspeechClient:

    def __init__(self, appid: str, token: str, cluster: str, callback_url: str | None):
        self.appid = appid
        self.token = token
        self.cluster = cluster
        self.submit_url = "https://openspeech.bytedance.com/api/v1/auc/submit"
        self.query_url = "https://openspeech.bytedance.com/api/v1/auc/query"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer; {self.token}",
        }
        self.callback_url = callback_url

    def submit(self, audio_url: str, uid: str):
        data = {
            "app": {"appid": self.appid, "token": self.token, "cluster": self.cluster},
            "user": {"uid": uid},
            "audio": {"format": "mp3", "url": audio_url},
            "additions": {
                "use_itn": "False",
                "with_speaker_info": "True",
                "enable_query": "True",
            },
            "request": {},
        }
        if self.callback_url is not None:
            data["request"]["callback"] = self.callback_url

        response = requests.post(self.submit_url, json=data, headers=self.headers)
        if response.status_code != 200:
            raise BytedanceOpenspeechClientError(
                message=response.text,
                status_code=response.status_code,
                service_code=None,
            )
        res_data = response.json()["resp"]
        res_code = res_data["code"]
        res_message = res_data["message"]
        if res_code != 1000:
            raise BytedanceOpenspeechClientError(
                message=res_message,
                status_code=response.status_code,
                service_code=res_code,
            )
        res_id: str = res_data["id"]
        return res_id
