from Markdown2docx import Markdown2docx
import logging

def run(Q9900_md_file_path, process_job):
    try:
        logging.info("writing Q9950_GetDocx")
        project = Markdown2docx(Q9900_md_file_path.replace('.md',''))
        project.eat_soup()
        project.save()

        logging.info("writing Q9950_GetDocx: done")

    except Exception as e:
        logging.info("Q9950_GetDocx: error during convert markdown to docx")
        logging.info(e)

