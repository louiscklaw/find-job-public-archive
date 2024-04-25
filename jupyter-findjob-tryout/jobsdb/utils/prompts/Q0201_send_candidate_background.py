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
        with open("./config/Q0201_send_candidate_background.md", "r") as f_candidate_background:
            temp_candidate_background = "".join(
                f_candidate_background.readlines())

        candidate_background_result = tp_session.SendQuestion(
            BEARER,
            ('''
Remember the text below as job-applicant background and reply "OK"

Text: """
{content}
"""
'''
             )
            .format(content=MakeMarkdownString.make(temp_candidate_background))
            .strip(),
        )
        logging.info("Q0201: candidate background done")
        log_to_text_file(
            log_path + "/Q0201_send_candidate_background_A.json",
            json.dumps(candidate_background_result),
        )

        process_job.appendJobMeta(
            {"Q0201_send_candidate_background":
             {"A": candidate_background_result}
             }
        )

    except Exception as e:
        print("error Q0201")
        print(e)
