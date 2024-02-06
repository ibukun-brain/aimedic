import json

import requests

from aimedic.utils.env_variable import get_env_variable


class AutoGonAI:
    def __init__(self, api_key=None):
        self.url = "https://api.autogon.ai/api/v1"
        self.api_key = get_env_variable("AUTOGONAI_API_KEY", "XXX-XXX")

    def gpt_4(self, message):
        """
        Chat with Autogon Chat Completion API using powerful variants of the GPT models.
        """
        url = self.url + "/services/chat/"
        headers = {
            "X-AUG-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {"message": message}

        try:
            r = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=60
            )
        except Exception as e:
            raise e

        resp = json.loads(r.text)
        return resp
