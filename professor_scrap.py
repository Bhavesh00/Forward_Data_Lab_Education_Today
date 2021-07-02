from __future__ import print_function
from pprint import pprint
import html2text
from urllib.request import urlopen
from googlesearch import search # https://pypi.org/project/googlesearch-python/

from database_controller import update_Professors_DB

'''
Go to Google. 
Search (name,institution). 
Filter results --> URLs that are faculty homepages.
'''
def query_urls(prof_list):
    
    for p_name, p_instituition in prof_list:
        query = p_name + " " + p_instituition

        print (search(query, lang="en", num_results=10))
        print ("\n")
# to search
professor_name = "Kevin Chen-Chuan Chang"
instituition = "UIUC"

prof_list = [(professor_name,instituition),("Jiawei Han",instituition)]

'''
Go through each page. 
Extract information: 
    -Biography
    -Education
    -Awards
    -Research interests
    -Publications
'''
def extract_information(p_url):
    import requests
    from bs4 import BeautifulSoup

    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    information_criteria = ["Education", "Biography","Professional Highlights", "Research Statement", "Honors"]
    infoDictionary = {}

    url = p_url
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    for ic in information_criteria:
        for heading in soup.find_all('h2'):
            if not ic in heading.text: continue
            info_packet = ""
            for sib in heading.find_next_siblings():
                if sib.name == "h2":
                    break
                else:
                    #print(ic)
                    info_packet+=" "+sib.text

            if ic in infoDictionary:
                infoDictionary[ic]+= info_packet
            else:
                infoDictionary[ic] = info_packet

    print(infoDictionary['Research Statement'])
    return infoDictionary


def google_knowledge_graph(query):
    """Example of Python client calling Knowledge Graph Search API."""
    import json
    import urllib

    # query_urls(prof_list)
    #api_key = open('.api_key').read()
    api_key = ""
    #query = "Jiawei Han"
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 20,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())
    for element in response['itemListElement']:
        pprint(element)
        exit()
        print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')


def main():
    test_url = "https://cs.illinois.edu/about/people/faculty/kcchang"
    test_url2 ="http://www.forwarddatalab.org/kevinccchang"
    test_url3="http://hanj.cs.illinois.edu/"

    kC_data = extract_information(test_url)

    val = [('Kevin C. Chang', kC_data['Biography'][0:255], kC_data['Honors'][0:255], kC_data['Education'][0:255], 'University of Illinois Urbana-Champaign')]

    update_Professors_DB(val)

if __name__ == "__main__":
    main()



    #html = open(test_url).read()
#     webUrl  =  urlopen(test_url)
#     print ("result code: " + str(webUrl.getcode()))

#     page_html =  webUrl.read()
#     h = html2text.HTML2Text()
#  # Ignore converting links from HTML
#     h.ignore_links = True
#     print(h.handle(page_html))
    #print(page_html)
    #print(html2text.html2text(page_html))

    # resource = urlopen(test_url3)
    # content = resource.read()
    # #charset = resource
    # content = content.decode('utf-8')

    # ascii_page = html2text.html2text(content)
    # print(ascii_page)
    # print(ascii_page.find("##"))