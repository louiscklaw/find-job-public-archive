import logging
#!/usr/bin/env python

import asyncio
import nest_asyncio
import random

from utils.JobsDBFetchAndGenEmail import *
from utils.GetEmail import *
from utils.GetEmail import test

nest_asyncio.apply()

# kw_list = ['regression testing','Testing Analyst','Quality Assurance Engineer','android','system test', 'regression test','computer science','logical mindset','UAT','test automation','automated test','github','docker','expressjs','nextjs','css','css3','Restful', 'ROS','mocha','STLC', 'SDLC', 'testing automation', 'automation testing', 'selenium', 'JIRA', 'QA', 'git', 'mobile app', 'web', 'puppeteer', 'playwright', 'appium', 'python', 'react', 'software validation', 'software testing', 'javascript', 'nodejs', 'IOT']
kw_list = ['WallStone Functional Tester']

random.shuffle(kw_list)

test()
