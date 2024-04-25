import coloredlogs, logging
#!/usr/bin/env python

import asyncio
import nest_asyncio
import random

from utils.JobsDBFetchAndGenEmail import *
from utils.GetEmail import *

nest_asyncio.apply()

coloredlogs.install()
logger = logging.getLogger(__name__)

kw_list = [
    'regression testing','Testing Analyst','Quality Assurance Engineer','android','system test','regression test','computer science',
    'logical mindset','UAT','test automation','automated test','github','docker','langchain',
    'expressjs','nextjs','css','css3','Restful','ROS','mocha',
    'STLC','SDLC','testing automation','automation testing','selenium','JIRA','QA',
    'git','mobile app','web','puppeteer','playwright','appium','python','react',
    'software validation','software testing','javascript','nodejs','IOT',"vagrant","yolo","ultralytics","google","cypress","selenium","cucumber"
    ]
# kw_list = ['Group Quality Assurance Manager - Ground']

random.shuffle(kw_list)

for kw in kw_list:
    try:
        logger.info(f"main.py: working on keyword: {kw}")

        hypen_chained_keyword = kw.replace(' ', '-')

        temp_result = asyncio.run(
            JobsDBFetchAndGenEmail(hypen_chained_keyword))

        # jod down
        # temp_result = {}
        with open('./temp.json', 'r+') as fo:
            json.dump(temp_result, fo)
            # temp_result = json.load(fo)

        logging.info("main: len(temp_result) -> " + str(len(temp_result)))
        # create Q9900, result.md
        GetEmail(temp_result)
        # GetEmail([
        #     {
        #       "job_title": "Mobile Developer (HK$40K - $50K+) (Ref. No.: 26836)",
        #       "job_company": "Global Executive Consultants Ltd.",
        #       "job_link": "https://hk.jobsdb.com/job/75279957?type=standout&ref=search-standalone#sol=c209f9153d4fb7517291198b5c797d256683f43c",
        #       "job_apply_link": "https://hk.jobsdb.com/job/75279957/apply#view-job",
        #       "job_salary": "$40,000 \u2013 $50,000 per month",
        #       "meta": {
        #         "search_using_keyword": "git",
        #         "source_website": "jobsdb"
        #       }
        #     }
        # ])

    except Exception as e:
        logger.error("main: error during search using keyword -> " + kw)
        raise e
