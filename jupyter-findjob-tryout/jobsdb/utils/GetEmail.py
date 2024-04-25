from playwright.async_api import async_playwright

import os
import sys
import json
import re
import asyncio
from pprint import pprint
import random
import logging

from utils import Q9950_GetDocx

from const import DEFAULT_DEMO_CONTENT
from utils.SendQuestion import TeamPromptAi
from utils.URIgnores import URIgnores
# from prompts import helloworld, MakeMarkdownString

# from utils.prompts import *
from utils.prompts import Q0001_init_bot, \
    Q0100_send_job_highlight, \
    Q0201_send_candidate_background, \
    Q0301_draft_email, \
    Q0401_review_email, \
    Q0105_filter_by_candiates_preferences, \
    Q0106_salary_mentioned, \
    Q0107_salary_check

from utils.ProjectPaths import helloworldProjectPaths, dilutePath
from utils.genPage import *
from utils.FetchJobDetail import *
from utils.JobsDBFetchAndGenEmail import *
from utils.CleanHistory import *

# Set up logging
logging.basicConfig(filename='logs/GetEmail.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

def MakeSurePathExist(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)


class ProcessJob:
    def diluteCompanyName(self, company_name):
        output = company_name
        output = output.replace('/','_')
        output = output.replace('\\','_')
        output = output.replace('(','_')
        output = output.replace(')','_')
        output = output.replace(' ','_')
        output = output.replace("__",'_')
        output = output.replace(".",'_')
        output = output.replace(",",'_')
        output = output.replace("$",'_')
        output = output.replace("|",'_')
        output = output.replace("+",'_')
        output = output.replace(":",'_')
        output = output.replace("-",'_')
        output = output.replace(".",'_')
        output = output.replace("__",'_')

        output = re.sub(r'\s+', '_', output)

        # re to replace the right most _
        output = re.sub(r'_+$', '', output)



        for i in range(1, 30):
            output = output.replace('__', '_')

        output = re.sub(r'_+$', '', output)

        return output.strip()

    def __init__(self, logging, search_using_keyword, source_website, job_link, job_company, job_salary, job_title, url_ignore, job):
        try:
            self.state = "init start"
            self.cooldown_after_done = True
            self.default_cooldown_time = 3

            self.cwd = os.path.abspath("/app/output/000_raw_result")
            self.screenshot_file_name = 'post.png'
            self.md_file_name = "Q9900_result.md"

            self.job = job

            self.search_using_keyword = search_using_keyword
            self.source_website = source_website
            self.job_link = job_link
            self.job_company = self.diluteCompanyName(job_company)
            self.job_salary = job_salary
            self.job_title = job_title
            self.url_ignore = url_ignore

            m = re.search(".*/(\d+)\?", job_link)
            self.job_id = m.group(1)

            self.diluted_source_path = dilutePath(
                self.source_website + "_" + self.job_id + "_" + self.job_title)

            self.portfolio_screenshot_link = '/cv'+"/" + \
                self.diluted_source_path + "/" + self.screenshot_file_name

            self.log_path = self.getLogPath()
            self.output_path = self.getOutputPath()
            self.screenshot_path = self.output_path

            self.Q9900_md_file_path = os.path.join(
                self.output_path, self.md_file_name)

            self.state = "init done"
            self.prepareResultPath()

            self.log_file_path = self.getLogPath()
            self.updateJobJson()

            self.meta_file_path = self.getLogPath()
            self.appendJobMeta({"hello": "world"})
            self.appendJobMeta({
                "search_using_keyword": self.search_using_keyword,
                "source_website": self.source_website,
                "job_link": self.job_link,
                "job_company": self.job_company,
                "job_salary": self.job_salary,
                "job_title": self.job_title,
            })
            self.appendJobMeta({"job": self.job})

        except Exception as e:
            print("init:error")
            print(e)

    def prepareResultPath(self):
        try:
            if not os.path.exists(self.cwd):
                os.makedirs(self.cwd)
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            if not os.path.exists(self.screenshot_path):
                os.makedirs(self.screenshot_path)

        except Exception as e:
            print('prepareResultPath:error')
            print(e)
            raise e
            sys.exit()

    def checkProcessedBefore(self, skip_check=False):
        try:
            if (skip_check== True):
                logging.warning('checkprocessedbefore: skip check active')
                return False

            logging.info('GetEmail: checking url_ignore')
            processed_before = self.url_ignore.isIgnored(self.job_link.split("?type")[0])
            if (processed_before):
                # no need cooldown as no question will be passed to GPT
                self.cooldown_after_done = False
            return processed_before

        except Exception as e:
            print(e)

    def getOutputPath(self):
        try:
            diluted_source_path = dilutePath(
                self.source_website
                + "_" + self.job_id + "_" + self.job_title)
            return os.path.join(self.cwd, self.job_company, diluted_source_path)
        except Exception as e:
            print('getOutputPath:Error')
            print(e)
            sys.exit()

    def getLogPath(self):
        try:
            diluted_source_path = dilutePath(
                self.source_website
                + "_" + self.job_id + "_" + self.job_title)
            return os.path.join(self.cwd, self.job_company, diluted_source_path)
        except Exception as e:
            print(e)
            sys.exit()

    def prepareWorkspacePath(self):
        try:
            MakeSurePathExist(self.getOutputPath())
            logging.info('GetEmail: prepareWorkspacePath done')
        except Exception as e:
            print(e)
            sys.exit()

    def fetchJobDetail(self):
        retry_count = 3
        for i in range(0,retry_count):
            try:
                if (i > 0):
                    logging.warning("fetchJobDetail:retrying")

                self.job_details = asyncio.run(FetchJobDetail(
                    self.job,
                    os.path.join(self.screenshot_path, self.screenshot_file_name)
                ))

                break
            except Exception as e:
                logging.error("fetchJobDetail:Error")
                print(e)

    def helloworld(self):
        print("helloworld")

    def gptInitialize(self):
        try:
            logging.info('GetEmail: start ask GPT')
            self.tp_session = TeamPromptAi()
            CleanHistory()

        except Exception as e:
            print(e)
            sys.exit()

    def gptSendQuestions(self):
        Q0001_init_bot.ask(self.log_path, self.tp_session, self)

        Q0100_send_job_highlight.ask(
            self.log_path,
            self.tp_session,
            self.job_link,
            self.job_company,
            self.job_title,
            self.job_details,
            self.job_salary,
            self)

        # send candidate background
        Q0201_send_candidate_background.ask(self.log_path, self.tp_session, self)

    def gptDecideGoAhead(self, force_go_ahead=False):
        if (force_go_ahead):
            return force_go_ahead

        go_ahead = True

        try:

            # show stopper by preferences
            # Yes -> it is related to IT / software
            # No -> it is not related to IT / software
            self.preference_check_result = Q0105_filter_by_candiates_preferences.ask( self.log_path, self.tp_session, self)
            logging.info('preference_check_result: ' + self.preference_check_result)
            if (self.preference_check_result.lower().find('yes') > -1):
                # job is it or software related
                pass
            else:
                logging.info('skip processing as preferences check failed')
                go_ahead = False

            self.check_salary_mentioned_in_job_detail_result = Q0106_salary_mentioned.ask( self.log_path, self.tp_session, self)
            logging.info('check_salary_mentioned_in_job_detail_result: ' + self.check_salary_mentioned_in_job_detail_result)

            # Yes -> mentioned salary in info given
            # No -> Not mentioned salary in info given
            if (self.check_salary_mentioned_in_job_detail_result.lower().find('yes') > -1):
                logging.info("as salary mentioned in job detail, check salary range")

                self.pass_salary_range_check = Q0107_salary_check.ask( self.log_path, self.tp_session, self)

                logging.info('pass_salary_range_check: '+self.pass_salary_range_check)

                if (self.pass_salary_range_check.lower().find('yes') > -1):
                    logging.info("job passed by salary range check")
                    pass
                else:
                    logging.info('skip processing by salary mentioned')
                    go_ahead = False
            else:
                logging.info('skip salary range check as not mentioned')

        except Exception as e:
            print(e)

        finally:
            if (not go_ahead):
                # skip cooldown as no question will be passed to GPT
                self.cooldown_after_done = False


        return go_ahead

    def gptProcessDraftContent(self):
        try:
            self.email_json = Q0301_draft_email.ask( self.log_path, self.tp_session, self)
            self.email_content = self.email_json["text"]

            # paraphasing, https://www.promptingguide.ai/techniques/tot, tree of thought
            # Then all experts will go on to the next step, etc.
            # If any expert realizes they're wrong at any point, they leave.
            self.review_result = Q0401_review_email.ask( self.log_path, self.tp_session, self.email_content, self)

        except Exception as e:
            print(e)

    def gptSendInputToGPT(self):
        retry_count = 3

        for i in range(0,retry_count):
          if(i > 0):
              logging.warning("error found, retrying")

          try:
              self.gptInitialize()

              self.gptSendQuestions()
              if (self.gptDecideGoAhead()):
                  self.gptProcessDraftContent()
                  self.gptFormatOutput()
              else:
                  logging.info('skip processing as gptDecideGoAhead results -> False')
                  self.skipProcessJob()

              break
          except Exception as e:
              logging.error("error during processing gptSendInputToGpt")
              print(e)


    def gptDecision_del(self):
        try:
            # show stopper by preferences
            stopped_by_preferences_check = Q0105_filter_by_candiates_preferences.ask(
                self.log_path, self.tp_session)
            logging.info('stopped_by_preferences_check: ' +
                         stopped_by_preferences_check)
            if (stopped_by_preferences_check != 'yes'):
                logging.info('skip processing by show stopper')
                self.skipProcessJob()

            Q0106_salary_mentioned.ask(
                self.log_path, self.tp_session)
            logging.info('stopped_by_salary_check: ' +
                         stopped_by_salary_check)
            if (stopped_by_salary_check != 'yes'):
                logging.info('skip processing by show stopper')
                self.skipProcessJob()

        except Exception as e:
            print(e)

    def gptFormatOutput(self):
        try:
            with open(self.Q9900_md_file_path, "a+") as f_out:
                f_out.truncate(0)
                f_out.writelines([self.email_content])
                f_out.writelines(["\n\n---\n\n"])
                f_out.writelines([self.review_result["text"]])
                f_out.writelines(["\n"])

            # write to portfolio page
            self.email_content = ExtractEmailBody(self.email_content)
            self.email_title = "Application letter for :" + self.job_title
            self.email_summary = self.job_company+','+self.search_using_keyword

            WriteMdx(
                self.output_path + "/Q9500_index.mdx",
                self.screenshot_file_name,
                self.job_company,
                self.email_content,
                DEFAULT_DEMO_CONTENT,
                self.email_title,
                self.email_summary,
            )

            WriteMdx(
                self.output_path + "/index.mdx",
                self.portfolio_screenshot_link,
                self.job_company,
                self.email_content,
                DEFAULT_DEMO_CONTENT,
                self.email_title,
                self.email_summary,
            )

            # create Q9950, convert markdown to docx
            Q9950_GetDocx.run(self.Q9900_md_file_path, self)

        except Exception as e:
            print(e)

    def addToUrlIgnoreHistory(self):
        try:
            self.url_ignore.addUrl(self.job_link.split("?type")[0])
        except Exception as e:
            logging.error(e)

    def skipProcessJob(self):
        try:
            logging.warning('skipProcessJob')

        except Exception as e:
            print(e)

    def sysExit(self, reason=""):
        logging.error(reason)
        sys.exit()

    def updateJobJson(self):
        try:
            # create file if not exist
            with open(os.path.join(self.log_file_path, 'jobs.json'), 'w+') as f:
                json.dump({
                    "job_link": self.job_link,
                    "job_company": self.job_company,
                    "job_salary": self.job_salary,
                    "job_title": self.job_title,
                    "search_using_keyword": self.search_using_keyword,
                    "source_website": self.source_website,
                }, f)

        except Exception as e:
            print('updateJobJson:error')
            print(e)
            sys.exit()

    def appendJobMeta(self, content_to_append):
        job_temp = {"questions":{}}

        try:
            # check if file exist
            if os.path.isfile(os.path.join(self.meta_file_path, 'meta.json')):
                with open(os.path.join(self.meta_file_path, 'meta.json'), 'r+') as f:
                    job_temp = json.load(f)

            # create file if not exist
            with open(os.path.join(self.meta_file_path, 'meta.json'), 'a+') as f:
                f.truncate(0)
                job_temp = {**job_temp, **content_to_append}
                json.dump(job_temp, f, indent=2)

        except Exception as e:
            print('appendJobMeta:error')
            print(e)
            sys.exit()


def GetEmail(result, max_successful_gen=10):
    successful_gen = 0

    for job in result:
        try:
            logging.info('GetEmail.py: start')

            job_meta = job["meta"]
            search_using_keyword = job_meta["search_using_keyword"]
            source_website = job_meta["source_website"]

            job_link = job["job_link"]
            job_company = job["job_company"]
            job_salary = job["job_salary"]
            job_title = job["job_title"]

            url_ignore = URIgnores()
            process_job = ProcessJob(
                logging,
                search_using_keyword,
                source_website,
                job_link,
                job_company,
                job_salary,
                job_title,
                url_ignore,
                job)

            if process_job.checkProcessedBefore():
                logging.warning("URL: " + job_link + " already in the list, skipping... ")
            else:
                # get jobdetail from web
                logging.info("process_job.fetchJobDetail()")
                process_job.fetchJobDetail()
                logging.info("process_job.prepareWorkspacePath()")
                process_job.prepareWorkspacePath()
                logging.info("process_job.gptSendInputToGPT()")
                process_job.gptSendInputToGPT()
                logging.info("process_job.addToUrlIgnoreHistory()")
                process_job.addToUrlIgnoreHistory()


            # complete before this line
            successful_gen = successful_gen + 1
            if successful_gen >= max_successful_gen:
                break
            else:
                if (process_job.cooldown_after_done):
                    logging.info("gen done")
                    logging.info(f'cool down {process_job.default_cooldown_time} seconds')
                    time.sleep(process_job.default_cooldown_time)

        except Exception as e:
            logging.error("GetEmail: error during processing " + job_link)
            logging.error(e)
            break

    logging.info("done")


# def test():
#     process_job = ProcessJob(
#         logging,
#         "keyword ?",
#         "www.jobsdb.com",
#         "https://hk.jobsdb.com/job/75167603?type=standout&ref=search-standalone#sol=d6e6fa3287e70377958d892fc6cfd421d812aeb7",
#         'a & b ', 'job_salary', 'job_title',
#         [], {})
#     print("helloworld")
