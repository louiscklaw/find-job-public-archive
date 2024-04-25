import os, sys
import requests
import json
import html2text
import logging

from utils.log import hello_world_log, log_to_text_file
# from utils.prompts_test import *

BEARER = os.getenv("BEARER", "not found")

def make(md_string):
    start = "```"
    end = "```"

    return start + md_string + end


def test(md_string):
    print("hello test")
