from playwright.async_api import async_playwright
import json
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)


async def FetchJobDetail(job, screenshot_path):
    logging.info("fetching job detail")

    try:

        job_link = job['job_link']

        logging.info(f'FetchJobDetail: fetching {job_link}')

        job_details = ''

        async with async_playwright() as pw:
            browser = await pw.firefox.launch(headless=True)
            page = await browser.new_page()

            await page.goto(job_link)
            title_element = await page.query_selector("title")
            title_text = await title_element.inner_text()

            temp = await page.evaluate("""
async () => {
temp=document.querySelectorAll(`[data-automation~="jobAdDetails"]`)[0].outerHTML

return JSON.stringify({job_details: temp});
        }
""")
            job_details = json.loads(temp)['job_details']

            await page.screenshot(path="last_screenshot.png", full_page=True)
            await page.screenshot(path=screenshot_path, full_page=True)
            await browser.close()

        logging.info('FetchJobDetail: done')

        return job_details

    except Exception as e:
        print(e)
        raise e
