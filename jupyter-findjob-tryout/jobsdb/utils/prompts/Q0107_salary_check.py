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
        with open("./config/Q0107_salary_check.md", "r") as f_preprompt:
            question = "".join(f_preprompt.readlines())

        team_review_q = ((
            '''
{question}
''').format(question=question).strip())

        Q0107_result = tp_session.SendQuestion(BEARER, team_review_q)
        Q0107_result = Q0107_result['text'].lower()

        logging.info('Q0107: result -> '+ Q0107_result)
        log_to_text_file(log_path + "/Q0107_result.json",
                         json.dumps(Q0107_result))
        process_job.appendJobMeta(
            {"Q0107_salary_range_check": {"Q": team_review_q, "A": Q0107_result}})

        Q0107_reason = tp_session.SendQuestion(BEARER, 'Explain your answer.')
        log_to_text_file(log_path + "/Q0107_reason.json",
                         json.dumps(Q0107_reason))
        process_job.appendJobMeta({"Q0107_reason": {"A": Q0107_reason}})

        if (Q0107_result.lower().find('yes') > -1):
            logging.info('Q0107: salary range check check shows positive, keep going')
        else:
            logging.warning("Q0107: salary range check negative")
            raise "terminated as failed salary range check"

        log_to_text_file(log_path + "/Q0107_result.json",
                         json.dumps(Q0107_result))

        logging.info("Q0107: done")

        return Q0107_result
    except Exception as e:
        print("Q0107: terminated by Q0107_salary_range_check")
        print(e)
        raise e
