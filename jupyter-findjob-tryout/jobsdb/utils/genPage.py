import os, sys
import json
import re
import logging

LETTER_HEAD = '''
<div style={{display: 'flex', alignItems: 'center'}}>
<CompanyHead>company_head</CompanyHead>
<OriginalPostLink href="png_path">original post</OriginalPostLink>
</div>
'''.strip()


FRONTMATTER = '''
title: {{title}}
publishedAt: '2021-09-26'
summary: {{summary}}
show: true
'''.strip()

def getLetterHead(company_head = 'company head', png_path = 'png_path'):
    return LETTER_HEAD.replace('company_head' , company_head).replace('png_path',png_path)

def getFrontmatter(title, summary):
    return FRONTMATTER.replace('{{title}}',title).replace('{{summary}}',summary)

def ExtractEmailBody(email_text):
    start_marker = "Dear"
    end_marker = "</sub>"

    start_index = email_text.find(start_marker)
    end_index = email_text.find(end_marker) + len(end_marker)

    if start_index != -1 and end_index != -1:
        email_text = email_text[start_index:end_index].strip()
        logging.info("ExtractEmailBody: content extracted")
    else:
        logging.info("ExtractEmailBody: Markers not found in the text.")

    return email_text

def WriteMdx(mdx_file_path, post_png_path = '',job_company='job_company', email_content="email_content blablabla",
             default_demo_content="",
             title="tt", summary="ss"):

    try:
        logging.info("WriteMdx: write to " + mdx_file_path)
        with open(mdx_file_path, 'a+') as f_out:
            f_out.truncate(0)
            f_out.writelines(['---\n'])
            f_out.writelines([getFrontmatter(title,summary)])
            f_out.writelines(['\n'])
            f_out.writelines(['\n---\n'])
            f_out.writelines(['\n'])
            f_out.writelines([getLetterHead(job_company, post_png_path)])
            f_out.writelines(['\n'])
            f_out.writelines(['\n---\n'])
            f_out.writelines(['\n'])
            f_out.writelines([email_content])
            f_out.writelines(['\n'])
            f_out.writelines(['\n---\n'])
            f_out.writelines(['\n'])
            f_out.writelines([default_demo_content])
            f_out.writelines(['\n'])

    except Exception as e:
        logging.error(e)

def HelloworldWriteMdx():
    print("helloworld write mdx")

# for testing
if __name__ =="__main__":
    from const_test import default_demo_content

    # jobsdb_73981461_Director / Deputy Director, Intelligent IoT System
    with open(r'D:\_workspace\find-job\jupyter-findjob-tryout\notebook\jobsdb\_output\appium\jobsdb_73986028_Software_Engineer_Automation_Testing\006_email_json.json','r') as f_json:
        temp_json = json.load(f_json)

    email_content = ''
    email_content = temp_json['text']

    email_content = ExtractEmailBody(email_content)
    job_company = 'bbbos fintech Limited'
    post_png = '/cv/diluted_source_path/post.png'
    result = WriteMdx('test.mdx', post_png,job_company, email_content, default_demo_content)


