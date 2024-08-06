import base64
import hashlib
import hmac
from pydantic import BaseModel
import requests
from datetime import datetime


class XunFeiAiPPTClient:

    class XunFeiAiPPTClientError(Exception):
        def __init__(self, message: str, status_code: int, service_code: str | None):
            self.message = message
            self.status_code = status_code
            self.service_code = service_code
            super().__init__(self.message)

        def __str__(self):
            return f"XunFeiAiPPTClientErrorError: {self.message} -- {self.status_code} -- {self.service_code}"

    def __init__(self, app_id: str, api_secret: str):
        self.app_id = app_id
        self.api_secret = api_secret

    def __md5(self, text: str):
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def __hmac_sha1_encrypt(self, encrypt_text: str, encrypt_key: str):

        return base64.b64encode(
            hmac.new(
                encrypt_key.encode("utf-8"), encrypt_text.encode("utf-8"), hashlib.sha1
            ).digest()
        ).decode("utf-8")

    def __get_signature(self, timestamp: int):
        auth = self.__md5(self.app_id + str(timestamp))
        return self.__hmac_sha1_encrypt(auth, self.api_secret)

    def __generate_headers(self):
        timestamp = int(datetime.timestamp(datetime.now()))
        signature = self.__get_signature(timestamp)

        headers = {
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature,
        }
        return headers

    class TaskInfo(BaseModel):
        sid: str
        coverImgSrc: str
        title: str
        subTitle: str

    def create_task_from_text(self, text: str):
        url = "https://zwapi.xfyun.cn/api/aippt/create"
        json = {"query": text}
        headers = self.__generate_headers()
        response = requests.post(url, json=json, headers=headers)
        if response.status_code != 200:
            raise XunFeiAiPPTClient.XunFeiAiPPTClientError(
                message=response.text,
                status_code=response.status_code,
                service_code=None,
            )
        response_data = response.json()
        if response_data["code"] != 0:
            raise XunFeiAiPPTClient.XunFeiAiPPTClientError(
                message=response_data["desc"],
                status_code=response.status_code,
                service_code=response_data["code"],
            )
        return XunFeiAiPPTClient.TaskInfo(**response_data["data"])

    class TaskProgress(BaseModel):
        process: int
        pptUrl: str | None
        errMsg: str | None

    def get_task_progress(self, sid: str):
        url = "https://zwapi.xfyun.cn/api/aippt/progress"
        prarms = {"sid": sid}
        headers = self.__generate_headers()
        response = requests.get(url, params=prarms, headers=headers)
        if response.status_code != 200:
            raise XunFeiAiPPTClient.XunFeiAiPPTClientError(
                message=response.text,
                status_code=response.status_code,
                service_code=None,
            )
        response_data = response.json()
        if response_data["code"] != 0:
            raise XunFeiAiPPTClient.XunFeiAiPPTClientError(
                message=response_data["desc"],
                status_code=response.status_code,
                service_code=response_data["code"],
            )
        return XunFeiAiPPTClient.TaskProgress(**response_data["data"])