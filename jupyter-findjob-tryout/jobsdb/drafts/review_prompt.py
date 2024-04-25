import os,sys

temp_review_preprompt = '''
## temp_review_preprompt
'''

email_content = '''
email_content
'''


print(
    '''
{review_preprompt}

Application letter:
"""
{email_content}
"""
'''.format(review_preprompt = temp_review_preprompt, email_content=email_content).strip()
)
