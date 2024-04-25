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


def ask(log_path, tp_session, job_link, job_company, job_title, job_details, job_salary, process_job):
    try:
        job_highlight_md = """
{job_link}

Company Name:{job_company}
Job Title:{job_title}
Salary:{job_salary}

{job_details}
        """.format(
            job_link=job_link,
            job_company=job_company,
            job_title=job_title,
            job_salary=html2text.html2text(job_salary),
            job_details=html2text.html2text(job_details),
        ).strip()

        question = (('''
Remember the text below as a job highlight and reply "OK"

Text: """
{content}
"""
''')
                    .format(content=MakeMarkdownString.make(job_highlight_md))
                    .strip())

        result = tp_session.SendQuestion(BEARER, question)

        logging.info("Q0100: send job highlight done")

        log_to_text_file(
            log_path + "/Q0100_send_job_highlight_Q.md", job_highlight_md)

        log_to_text_file(
            log_path + "/Q0100_send_job_highlight_A.json", json.dumps(result)
        )

        process_job.appendJobMeta(
            {"Q0100_send_job_highlight": {
                "Q": job_highlight_md,
                "Q_prettify": job_highlight_md.split('\n'),
                "A": result
            }}
        )

    except Exception as e:
        logging.error("error Q0100_send_job_highlight")
        print(e)
