import requests
import html2text
import re
text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
text_maker.bypass_tables = False
text_maker.UNICODE_SNOB = True
text_maker.ESCAPE_SNOB = True
text_maker.IGNORE_IMAGES = True


def extract(url):
    response = requests.request("GET", url)
    html = response.text.encode('utf8')
    html = str(html.decode("utf8"))
    text = text_maker.handle(html)
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('\\n', ' ').replace('\\', ' ')
    text = re.sub(' +', ' ', text)
    return text