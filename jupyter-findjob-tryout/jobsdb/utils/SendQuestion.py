import os
import sys
import json
import logging
import requests

from const import num

logging.basicConfig(level=logging.INFO)


class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start_engine(self):
        logging.info("Engine started!")

    def stop_engine(self):
        logging.info("Engine stopped.")


class TeamPromptAi:
    def __init__(self):
        self.c_id = ""

    def SendQuestion(self, BEARER, question):
        try:
            url = "https://gptapi.apoidea.ai/v1/conversation/conversations"
            if self.c_id != "":
                url = (
                    "https://gptapi.apoidea.ai/v1/conversation/conversations/"
                    + self.c_id
                    + "/messages"
                )
            headers = {
                "accept": "text/event-stream",
                "authority": "gptapi.apoidea.ai",
                "accept-language": "en-US,en;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7,zh;q=0.6",
                "authorization": BEARER,
                "cache-control": "no-cache",
                "content-type": "application/json",
                "origin": "https://teamprompt.ai",
                "pragma": "no-cache",
                "referer": "https://teamprompt.ai/",
                "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            }

            data = {"prompt": question, "stream": False}

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                self.c_id = response.json()["conversationId"]
                return response.json()

            else:
                logging.error(
                    "POST request failed with status code: %s", response.status_code
                )
                raise Exception("error during sending question to GPT")

        except Exception as e:
            logging.exception("error found during sending question")
            logging.debug(question)
            sys.exit()


