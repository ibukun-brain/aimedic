import json

import requests

from aimedic.utils.env_variable import get_env_variable

AUTOGONAI_CHATBOT_AGENT_ID = get_env_variable("AUTOGONAI_CHATBOT_AGENT_ID")


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

    def chatbot_agent(self, question):
        """
        This API allows seamless communication between a client application
        and a custom chatbot service agent, facilitating natural language
        processing and response generation.
        """
        url = self.url + f"/services/chatbot/{AUTOGONAI_CHATBOT_AGENT_ID}/chat/"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "question": question,
            # "session_id": session_id,
        }

        try:
            r = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=60
            )
        except Exception as e:
            raise e

        resp = json.loads(r.text)
        return resp
