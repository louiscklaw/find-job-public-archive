#!/usr/bin/env python3

import os, sys
import json

url = "https://gptapi.apoidea.ai/v1/conversation/conversations"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "text/event-stream",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://teamprompt.ai/",
    "Content-Type": "application/json",
    "Authorization": os.getenv("BEARER"),
    "Origin": "https://teamprompt.ai",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}

num = 0

default_demo_content = '''
#### Simple Application test demo

#### Purpose

This is a simple "helloworld" test script for testing Hong Kong Observatory mobile application demo.

It use appium, javascript and android emulator to conduct the test.

If you have any ideas that doesn't found demonstrated please let me know.

#### Demo

<iframe
  className="shadow"
  width="100%"
  height="600px"
  src="https://www.youtube.com/embed/2fMBSod31ao"
  title="YouTube video player"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowFullScreen>
</iframe>
'''
