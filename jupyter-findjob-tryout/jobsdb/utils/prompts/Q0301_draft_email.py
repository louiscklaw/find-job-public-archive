import os
import sys
import requests
import json
import html2text
import logging

from utils.log import hello_world_log, log_to_text_file
# from utils.prompts_test import *
from utils.prompts import MakeMarkdownString

BEARER = os.getenv("BEARER", "not found")

def ask(log_path, tp_session, process_job):
    try:
        with open("./config/Q0301_draft_email.md", "r") as f_email_preprompt:
            temp_email_preprompt = "".join(f_email_preprompt.readlines())

        send_email_result = tp_session.SendQuestion(
            BEARER,
            ('''{content}''')
            .format(content=MakeMarkdownString.make(temp_email_preprompt))
            .strip(),
        )
        question = ('''{content}''').format(
            content=MakeMarkdownString.make(temp_email_preprompt)).strip()
        log_to_text_file(log_path + "/Q0301_draft_email_A.json",
                         json.dumps(send_email_result))

        email_json = tp_session.SendQuestion(BEARER, """draft me a email""")
        log_to_text_file(log_path + "/Q0301_draft_email_Q.json",
                         json.dumps(email_json))

        process_job.appendJobMeta({"Q0301_draft_email": [
            {
                "Q": question,
                "A": send_email_result,
                "Q_prettify": question.split('\n'),
            },
            {
                "email_json": email_json,
                "email_json_prettify": email_json['text'].split('\n'),
            },
        ]})

        logging.info('Q0301: send email done')
        return email_json
    except Exception as e:
        logging.info("Q0301: Q0301_draft_email")
        logging.info(e)
