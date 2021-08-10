from bs4 import BeautifulSoup, NavigableString, Comment
import requests
import re
from collections import OrderedDict


# Get HTML and remove tags that does not contain useful information
def get_connection(url):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
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
                # print(temp)
                str1 = ' '.join(temp)
                # print(str1)
                res.append(str1)

    raw_data = list(OrderedDict.fromkeys(res))
    return raw_data


# Cleaning data according to different text user want
def data_process(raw_data, mode='na'):
    if mode == 'research':
        # Remove text with number
        raw_data = [line for line in raw_data if not re.match(r'.*[0-9].*', line)]

    if mode == 'bio' or mode == 'award':
        # Remove text with 1 or 2 words or chars |^\S*\s*\S*$
        raw_data = [line for line in raw_data if not re.match(r'^\S*$', line)]

    # Remove multiple space
    raw_data = [re.sub(r'\s+', ' ', line, flags=re.I) for line in raw_data]

    print(len(raw_data))

    # Remove duplicate text
    raw_data = list(OrderedDict.fromkeys(raw_data))

    print(len(raw_data))

    return raw_data


if __name__ == '__main__':

    # Test list of researcher homepage URL
    url_list = [
        'https://cs.illinois.edu/about/people/all-faculty/zaher',
        # 'https://cs.illinois.edu/about/people/all-faculty/sadve',
        # 'https://cs.illinois.edu/about/people/all-faculty/angrave',
        # 'https://cs.illinois.edu/about/people/all-faculty/mdbailey',
        # 'https://cs.illinois.edu/about/people/all-faculty/mattox',
        # 'https://cs.illinois.edu/about/people/all-faculty/nikita',
        # 'https://cs.illinois.edu/about/people/all-faculty/tbretl'
        # 'https://cs.illinois.edu/about/people/all-faculty/rhc'
        # 'https://cs.illinois.edu/about/people/all-faculty/karthe',
        # 'https://cs.illinois.edu/about/people/all-faculty/kcchang',
        # 'https://cs.illinois.edu/about/people/all-faculty/dchen',
        # 'https://cs.illinois.edu/about/people/all-faculty/girishc',
        # 'https://cs.illinois.edu/about/people/all-faculty/minhdo',
        # 'https://cs.illinois.edu/about/people/all-faculty/dullerud',
        # 'https://cs.illinois.edu/about/people/all-faculty/melkebir',
        # 'https://cs.illinois.edu/about/people/all-faculty/jeffe',
        # 'https://cs.illinois.edu/about/people/all-faculty/waf',
        # 'https://cs.illinois.edu/about/people/all-faculty/jugal',
        # 'https://cs.illinois.edu/about/people/all-faculty/pbg',
        # 'https://cs.illinois.edu/about/people/all-faculty/mgolpar',
        # 'https://cs.illinois.edu/about/people/all-faculty/wgropp',
        # 'https://cs.illinois.edu/about/people/all-faculty/jhasegaw',
        # 'https://cs.illinois.edu/about/people/all-faculty/kkhauser',
        # 'https://cs.illinois.edu/about/people/all-faculty/heath',
        # 'https://cs.illinois.edu/about/people/all-faculty/dhoiem',
        # 'https://cs.illinois.edu/about/people/all-faculty/jianh',
        # 'https://cs.illinois.edu/about/people/all-faculty/w-hwu',
        # 'https://cs.illinois.edu/about/people/all-faculty/rkiyer',
        # 'https://cs.illinois.edu/about/people/all-faculty/hengji',
        # 'https://cs.illinois.edu/about/people/all-faculty/jiang56',
        # 'https://www.cs.princeton.edu/people/profile/tomg',
        # 'https://www.cs.princeton.edu/people/profile/aartig',
        # 'https://www.cs.princeton.edu/people/profile/ehazan',
        # 'https://www.cs.princeton.edu/people/profile/fheide',
        # 'https://www.cs.princeton.edu/people/profile/kylej',
        # 'https://www.cs.princeton.edu/people/profile/ak18',
        # 'https://www.cs.princeton.edu/people/profile/bwk',
        # 'https://www.cs.princeton.edu/people/profile/zkincaid',
        # 'https://www.cs.princeton.edu/people/profile/gkol',
        # 'https://www.cs.princeton.edu/people/profile/aalevy',
        # 'https://www.cs.princeton.edu/people/profile/dl9',
        # 'https://www.cs.princeton.edu/people/profile/appel',
        # 'https://www.cs.princeton.edu/people/profile/dpd',
        # 'https://www.cs.princeton.edu/people/profile/rdondero',
        # 'https://www.cs.princeton.edu/people/profile/zdvir',
        # 'https://www.cs.princeton.edu/people/profile/bee',
        # 'https://www.cs.princeton.edu/people/profile/fellbaum',
        # 'https://www.cs.princeton.edu/people/profile/felten',
        # 'https://www.cs.princeton.edu/people/profile/af',
        # 'https://www.cs.princeton.edu/people/profile/rfish',
        # 'https://www.cs.princeton.edu/people/profile/mfreed',
        # 'https://www.cs.princeton.edu/people/profile/maia',

        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/abbeel.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/asanovic.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/ayazifar.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bachrach.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bajcsy.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/mball.html', #
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/dbamman.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/barsky.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bartlett.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/bayen.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/blum.html', #
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/borgs.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/brewer.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/aydin.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/canny.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/jchayes.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/akcheung.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/alexch.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/clancy.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/colella.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/ncrooks.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/culler.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/darrell.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/demmel.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/denero.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/anca.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/prabal.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/efros.html', #
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/elghaoui.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hfarid.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/harrison.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hartmann.html', #
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/harvey.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hearst.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hellerstein.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/hilfinger.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/joshhug.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/nilah.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/jiantao.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/jordan.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/joseph.html',
        # 'https://www2.eecs.berkeley.edu/Faculty/Homepages/kahan.html'
    ]

    # append new data to current dataset
    db = []
    for url in url_list:
        soup = get_connection(url)
        raw = get_raw_data(soup)
        data = data_process(raw)
        db.extend(data)
    print(db)
    # with open('corpus', 'a') as fd:
    #     for data in db:
    #         data = data + ' 0\n'
    #         fd.writelines(data)
