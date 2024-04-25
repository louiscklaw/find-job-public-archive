import os, sys
import requests
import json
import html2text
import logging

from utils.log import hello_world_log, log_to_text_file
# from utils.prompts_test import *

BEARER = os.getenv("BEARER", "not found")

def ask(log_path, tp_session, process_job):
    try:
        with open("./config/Q0001_init_bot_preprompt.md", "r") as f_general_preprompt:
            temp_general_preprompt = "".join(f_general_preprompt.readlines())

        # init bot
        init_bot_result = tp_session.SendQuestion(BEARER, temp_general_preprompt)

        log_to_text_file(
            log_path + "/Q0001_init_bot_Q.json", json.dumps(temp_general_preprompt)
        )
        log_to_text_file(log_path + "/Q0001_init_bot_A.json", json.dumps(init_bot_result))

        process_job.appendJobMeta(
          {"Q0001_init_bot": {
              "Q": temp_general_preprompt,
              "Q_prettify": temp_general_preprompt.split('\n'),
              "A": init_bot_result
          }}
        )

        logging.info("Q0001: init bot done")
    except Exception as e:
        logging.error("error Q0001")
        logging.exception(e)

