from playwright.async_api import async_playwright
import os,sys, json, re
from pprint import pprint

async def JobsDBFetchAndGenEmail(kw="appium"):
    job_fetched = []
    async with async_playwright() as pw:
        browser = await pw.firefox.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://hk.jobsdb.com/{kw}-jobs".format(kw=kw))

        title_element = await page.query_selector("title")
        title_text = await title_element.inner_text()

        await page.screenshot(path="last_screenshot.png", full_page=True)

        result = await page.evaluate("""async () => {
            temp=[];
            document.querySelectorAll(`article`).forEach(el => {
                // grab all article elements
                // article_el = el.parentElement.parentElement
                try {
                    article_el = el;
                    console.log(article_el);
                    job_title = article_el.querySelector('h3').textContent ;
                    job_company = article_el.querySelector(`[data-automation~="jobCompany"]`).textContent;

                    job_salary = "not mentioned";
                    if (article_el.querySelector(`[data-automation~="jobSalary"]`)) {
                        job_salary = article_el.querySelector(`[data-automation~="jobSalary"]`).textContent;
                    }

                    job_link = article_el.querySelector(`a`).href;
                    // https://hk.jobsdb.com/job/74769655/apply#view-job
                    job_apply_link = article_el.querySelector(`a`).href.split('?')[0] + "/apply#view-job";
                    temp.push({job_title,job_company, job_link, job_apply_link, job_salary});
                } catch (error) {
                    console.log(el);
                }
            });
            return JSON.stringify(temp);
        }""")

        await browser.close()

        job_fetched = json.loads(result)
        for job in job_fetched:
            job['meta']={}
            job['meta']['search_using_keyword'] = kw
            job['meta']['source_website'] = 'jobsdb'

    return job_fetched
