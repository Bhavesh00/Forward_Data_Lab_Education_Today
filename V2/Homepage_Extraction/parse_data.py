from bs4 import BeautifulSoup, NavigableString, Comment
import requests
import re
from collections import OrderedDict

# Get HTML after removing useless tags
def get_connection(url):
    # Set user specifications for request to url
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    # Create request to url
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    # Access url with request and create BS HTML object for parsing
    soup = BeautifulSoup(r.text, "html.parser")
    # Remove tags with useless information
    for item in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'script', 'header', 'footer', 'nav', 'aside']):
        item.clear()

    return soup

# Get strings from HTML and combine sentence that different part under different tags
# for example the situation like <li>'xyz'<p>abc<\p>'123'<\li> will be combine to 'xyzabc123' instead of three strings
def get_raw_data(soup):
    res = []
    for tag in soup.find_all(re.compile('^li$|^p$|^div$|^tr$')):
        if tag.string and not tag.string.isspace():
            res.append(tag.string.strip())
        else:
            temp = []
            for des in tag.descendants:
                if des.name == 'ul' or des.name == 'li' or des.name == 'div':
                    break
                if isinstance(des, NavigableString) and not isinstance(des, Comment) and not des.isspace():
                    temp.append(des.strip())
            if len(temp) != 0:
                str1 = ' '.join(temp)
                res.append(str1)

    raw_data = list(OrderedDict.fromkeys(res))
    return raw_data

# Cleaning data based on data category/mode
def process_data(raw_data, mode='na'):
    if mode == 'research':
        # Remove text with number
        raw_data = [line for line in raw_data if not re.match(r'.*[0-9].*', line)]
    if mode == 'bio' or mode == 'award':
        # Remove text with 1 or 2 words or chars |^\S*\s*\S*$
        raw_data = [line for line in raw_data if not re.match(r'^\S*$', line)]

    # Remove multiple space
    raw_data = [re.sub(r'\s+', ' ', line, flags=re.I) for line in raw_data]
    # Remove duplicate text
    raw_data = list(OrderedDict.fromkeys(raw_data))

    return raw_data