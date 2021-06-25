from __future__ import print_function
from pprint import pprint

from googlesearch import search # https://pypi.org/project/googlesearch-python/

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

    information_criteria = ["Biography", "Education","Awards", "Research interests", "Publications"]



    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    url = p_url
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    target = soup.find("h2",text = "Biography")
    i = 0
    if target:
        for sib in target.find_next_siblings():
            if sib.name == "h2":
                break
            else:
                print("\n",sib.text)



def google_knowledge_graph(query):
    """Example of Python client calling Knowledge Graph Search API."""
    import json
    import urllib

    # query_urls(prof_list)
    #api_key = open('.api_key').read()
    api_key = "AIzaSyC26XthU72YUZjxf_0nK50UTmCPfoO7vzw"
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
    extract_information(test_url)


if __name__ == "__main__":
    main()