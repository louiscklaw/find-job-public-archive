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

        with open("./config/Q0105_filter_by_candiates_preferences.md", "r") as f_preprompt:
            question = "".join(f_preprompt.readlines())

        team_review_q = ((
            '''
{question}
''').format(question=question).strip())

        Q0105_result = tp_session.SendQuestion(BEARER, team_review_q)
        Q0105_result = Q0105_result['text'].lower()
        logging.info('Q0105: result -> '+Q0105_result)
        log_to_text_file(log_path + "/Q0105_result.json",
                         json.dumps(Q0105_result))

        process_job.appendJobMeta(
            {"Q0105_filter_by_candiates_preferences":
             {"Q": team_review_q, "A": Q0105_result}
             }
        )

        Q0105_reason = tp_session.SendQuestion(BEARER, 'Explain your answer')
        log_to_text_file(log_path + "/Q0105_reason.json",
                         json.dumps(Q0105_reason))
        process_job.appendJobMeta(
            {"Q0105_reason": {"Q0105_reason": Q0105_reason}})

        if (Q0105_result.lower().find('yes') > -1):
            logging.info(
                'Q0105: candiate preferences check shows positive, go ahead')
        else:
            logging.warning("Q0105: preferences check negative")
            raise "terminated as not suiteable for candiate"

        logging.info("Q0105: filter_preferences done")
        return Q0105_result
    except Exception as e:
        print("Q0105: terminated by Q0105_filter_by_candiates_preferences")
        print(e)
        raise e
