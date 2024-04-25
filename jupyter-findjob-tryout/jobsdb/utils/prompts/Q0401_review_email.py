import os
import sys
import requests
import json
import html2text
import logging

from utils.log import hello_world_log, log_to_text_file
# from utils.prompts_test import *

BEARER = os.getenv("BEARER", "not found")


def ask(log_path, tp_session, email_content, process_job):

    try:
        with open("./config/Q0401_review_email.md", "r") as f_review_preprompt:
            temp_review_preprompt = "".join(f_review_preprompt.readlines())

        team_review_q = ((
            '''
{review_preprompt}

Application letter: """
{email_content}
"""
''').format(review_preprompt=temp_review_preprompt, email_content=email_content).strip())

        review_result = tp_session.SendQuestion(BEARER, team_review_q)
        log_to_text_file(log_path + "/Q0401_review_email_Q.json",
                         json.dumps(team_review_q))
        log_to_text_file(log_path + "/Q0401_review_email_A.json",
                         json.dumps(review_result))

        process_job.appendJobMeta({"Q0401_review_email": {
            "Q": team_review_q,
            "Q_prettify": team_review_q.split('\n'),
            "A": review_result,
            "A_prettify": review_result['text'].split('\n'),
        }})

        logging.info("Q0401: review_email done")
        return review_result
    except Exception as e:
        logging.info("Q0401: terminated by Q0401_review_email")
        logging.info(e)
