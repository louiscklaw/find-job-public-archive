import requests
import json
import logging
import random
import time
import os
import sys

logger = logging.getLogger(__name__)

temp_preprompt = ""

if os.getenv('BEARER') == None or os.getenv("BEARER") == "":
    logger.error("authorization is missing")
    sys.exit(1)


url = "https://gptapi.apoidea.ai/v1/conversation/conversations"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "text/event-stream",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://teamprompt.ai/",
    "Content-Type": "application/json",
    "Authorization": os.getenv("BEARER"),
    "Origin": "https://teamprompt.ai",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}

def CleanHistory():
    try:
        logger.info("clean history start")
        response = requests.get(url, headers=headers)

        logger.info("got response")
        y = json.loads(response.text)
        conversationIds = list(map(lambda x: x["conversationId"], y))

        logger.info(f"got conversationIds. conversationIds={conversationIds}")

        if len(conversationIds) < 1:
            logger.info("no chat history to clear")

        for c_id in conversationIds:
            delay = random.uniform(0, 0.3)
            time.sleep(delay)

            logger.info(f"clearing conversation with id: {c_id}")

            delete_url = (
                f"https://gptapi.apoidea.ai/v1/conversation/conversations/{c_id}"
            )
            response = requests.delete(delete_url, headers=headers)

        logger.info("clean history done")

    except Exception as e:
        logger.error(f"error: {e}")
        raise e


