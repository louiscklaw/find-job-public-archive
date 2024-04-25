import os
import sys
import requests
import json
import html2text
import logging

from utils.log import hello_world_log, log_to_text_file
# from utils.prompts_test import *

BEARER = os.getenv("BEARER", "not found")


def ask(log_path, tp_session, process_job):
    question = ''

    try:
        with open("./config/Q0106_salary_mentioned.md", "r") as f_preprompt:
            question = "".join(f_preprompt.readlines())

        team_review_q = ((
            '''
{question}
''').format(question=question).strip())

        Q0106_result = tp_session.SendQuestion(BEARER, team_review_q)
        Q0106_result = Q0106_result['text'].lower()
        logging.info('Q0106: result -> '+Q0106_result)
        log_to_text_file(log_path + "/Q0106_result.json",
                         json.dumps(Q0106_result))
        process_job.appendJobMeta(
            {"Q0106_salary_mentioned": {"Q": team_review_q, "A": Q0106_result}})

        if (Q0106_result.lower().find('yes') > -1):
            logging.info('Q0106: salary mentioned in job details')
        else:
            logging.warning("Q0106: salary NOT mentioned in job details")

        log_to_text_file(log_path + "/Q0106_result.json",
                         json.dumps(Q0106_result))

        logging.info("Q0106: filter_preferences done")
        return Q0106_result
    except Exception as e:
        print("Q0106: terminated by Q0106_salary_mentioned")
        print(e)
        raise e
