import os, sys
import requests
import json
import html2text
import logging

from utils.log import hello_world_log, log_to_text_file
# from utils.prompts_test import *

BEARER = os.getenv("BEARER", "not found")

def MakeMarkdownString(md_string):
    start = "```"
    end = "```"

    return start + md_string + end




def Q0105_filter_by_candiates_preferences(log_path, tp_session):

    try:
        question = ''

        with open("./config/Q0105_filter_by_candiates_preferences.md", "r") as f_preprompt:
            question = "".join(f_preprompt.readlines())

        team_review_q = (('''
{question}
''').format(question=question).strip())

        Q0105_result = tp_session.SendQuestion(BEARER, team_review_q)
        Q0105_result = Q0105_result['text'].lower()
        print('Q0105: result -> '+Q0105_result)
        log_to_text_file(log_path + "/Q0105_result.json", json.dumps(Q0105_result))

        if (Q0105_result.lower().find('yes') > -1):
            print('Q0105: candiate preferences check shows positive, go ahead')
        else:
            Q0105_terminate_reason = tp_session.SendQuestion(BEARER, 'why ? briefly state the reason in 50 words or less')
            print('Q0105_terminate_reason:'+Q0105_terminate_reason)
            log_to_text_file(log_path + "/Q0105_terminate_reason.json", json.dumps(Q0105_terminate_reason))

            raise "terminated as not suiteable for candiate"

        log_to_text_file(log_path + "/Q0105_result.json", json.dumps(Q0105_result))

        print("Q0105: filter_preferences done")
        return Q0105_result
    except Exception as e:
        print("Q0105: terminated by Q0105_filter_by_candiates_preferences")
        print(e)
        raise e
