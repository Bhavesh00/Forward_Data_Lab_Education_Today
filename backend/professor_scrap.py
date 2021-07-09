from __future__ import print_function
from logging import info
from pprint import pprint
import html2text
from urllib.request import urlopen
from googlesearch import search  # https://pypi.org/project/googlesearch-python/

from database_controller import update_Professors_DB


class Professor:
    def __init__(self, professor_name, institution):
        self.name = professor_name
        self.institution = institution

        self.webpages = []
        self.biography = ""
        self.education = ""
        self.awards = ""
        self.research_interests = ""

    def update_urls(self, url):
        self.webpages.extend(url)

    def update_bio(self, biography_info_block):
        if len(self.biography) > 0:
            self.biography += " * "
        self.biography += biography_info_block

    def update_education(self, education_info_block):
        if len(self.education) > 0:
            self.education += " * "
        self.education += education_info_block

    def update_awards(self, awards_info_block):
        if len(self.awards) > 0:
            self.awards += " * "
        self.awards += awards_info_block

    def update_research_interests(self, research_interests_info_block):
        if len(self.research_interests) > 0:
            self.research_interests += " * "
        self.research_interests += research_interests_info_block

    def update_info_block(self, data_field, info_block):
        if data_field == 'biography':
            self.update_bio(info_block)
        if data_field == 'education':
            self.update_education(info_block)
        if data_field == 'awards':
            self.update_awards(info_block)
        if data_field == 'research_interests':
            self.update_research_interests(info_block)

    def print_brief(self):
        print("\nName: ", self.name)
        print("\nInstitution: ", self.institution)
        # print("\nEducation: ", self.education)
        # print("\nAwards: ", self.awards)
        print("\nResearch Interests: ", self.research_interests)
        print("\nBiography: ", self.biography)
        print("\n")


#  ['Awards', 'ACM Fellow', 'Fellow', 'Turing', 'ACM', 'IEEE', 'Achievements', 'Award', 'Prize', 'Fellowship', 'Membership']
data_field_dictionary = {
    'biography': ['Biography', 'Bio', 'About', 'About Me', 'Interest', 'Work', 'cirriculum vitae'],
    'education': ['Education', 'Study', 'Graduated'],
    'awards': ['Awards', 'Honors'],
    'research_interests': ['Research Interests', 'Research', 'Interest', 'Focus Area', 'Focus']
}
# Driver Function to read in the list of professors:

# Workflow-|
# We get a list of professors in the form (professor_name, institution)
# Our Goal is to go from this list of professors to a dictionary for the given professor_name,institution pair as key to dictionary of all the data fields, which each holds string values
# We have another way to convert from a list of synonyms to the

# We can take a single professor in an instance in the for loop, and now we want to get top url pages, and then parse each webpage individually for each of the data categories
# So for a given professor we will do a top 5 webpages search and pull the data of the 5 categories


# Two phases:
# Phase 1 is when the code goes throguh the lis tof professors and then finds the handful of urls for which we will scrap info of a professor.
# We then iterate through the urls for a given professor and then form a dictionary for the professor

# So we have a method that takes in the (prof_name, instituation, url_list**5 urls**)--> returns a dictionary with the standaradized keys     -Biograph ,Education, Awards, Research. --> this returned dictionary wil then be saved in a master dictionary with key (prof_name, instituation).

# Phase 2
# This master dictionary is then used to write to the db

# So we need one function to iterate through the list of professors for phase 1. Then there are two functions within this phase 1 driver, it will go professor by professor and pick up the top 5 urls. This picking is done by function 1. We are aiming to create data packet for a single
# Function 1: pick and return top 5 urls for a professor as list of strings.
# Once this list is returned it can immediately be used to parse for information.


'''
Phase 1
- We need to iterate through a list of (prof_name, institutions) 
- For a tuple we need to obtain 5 urls and form a 3-tuple with list of these urls and the above tuple
- Then we need to iterate through all the urls in the list in another driver function and do a webpage scrap for each 
'''


def audit_professors(professor_list):
    master_list = []
    # Iterate through list of provided professors,institution pairs.
    for professor_name, institution in professor_list:
        # Create a professor object
        my_professor = Professor(professor_name, institution)
        # For each pair we want to pull top 5 relevant webpages.
        query_urls(my_professor)
        # Scrap for information
        extract_information(my_professor)
        # Add the populated professor data packet to master list for DB exporting.
        master_list.append(my_professor)

    return master_list


'''
Go to Google. 
Search (name,institution). 
Filter results --> URLs that are faculty homepages.
'''


def query_urls(professor):
    query = professor.name + ", " + professor.institution
    temp_list = search(query, 10, "en")
    p_urls = []

    for url in temp_list:
        if ".edu" in url or ".org" in url:
            p_urls.append(url)

        if len(p_urls) == 3:
            break
    professor.update_urls(p_urls)


'''
Go through each page. 
Extract information: 
    -Biography
    -Education
    -Awards
    -Research interests
'''


def extract_information(professor):
    import requests
    from bs4 import BeautifulSoup

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    # Iterate through the list of urls for a given professor
    for url in professor.webpages:
        # create a request for given webpage
        req = requests.get(url, headers)
        # create a BeautifulSoup object to parse html
        soup = BeautifulSoup(req.content, 'html.parser')

        # Iterate through each of the info criteria we want to parse for
        for ic in data_field_dictionary.keys():
            # Iterate through each of the synonimous terms in our data_field_dictionary
            for sim_term in data_field_dictionary[ic]:
                # Now begin parsing h2 tags for the given url, searching for every similar_term of our information criteria
                for heading in soup.find_all('h2'):
                    if not sim_term.lower() in heading.text.lower(): continue

                    info_packet = ""
                    for sib in heading.find_next_siblings():
                        if sib.name == "h2":
                            break
                        else:
                            if len(info_packet) != 0:
                                info_packet += " "

                            new_add = sib.text.strip().replace('\xa0', " ").replace('\n', " ")
                            info_packet += new_add

                    professor.update_info_block(ic, info_packet)


def google_knowledge_graph(query):
    """Example of Python client calling Knowledge Graph Search API."""
    import json
    import urllib

    # query_urls(prof_list)
    # api_key = open('.api_key').read()
    api_key = ""
    # query = "Jiawei Han"
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
    home_prof = 'Kevin C. Chang'
    home_uni = 'University of Illinois Urbana-Champaign'

    p1 = (home_prof, home_uni)
    p2 = ('Geoffrey Challen', home_uni)
    p3 = ('Margaret M. Fleck', home_uni)
    p4 = ('David Forsyth', home_uni)
    p5 = ('David Cheriton', 'Stanford University')

    professor_list = [p1, p2]

    extracted_professors = audit_professors(professor_list)

    # for p in extracted_professors:
    #     p.print_brief()

    update_Professors_DB(extracted_professors)


if __name__ == "__main__":
    main()

###############################################################

# def query_urls(prof_list):

#     for p_name, p_instituition in prof_list:
#         query = p_name + " " + p_instituition

#         print (search(query, lang="en", num_results=10))
#         print ("\n")
# # to search

# prof_list = [(professor_name,instituition),("Jiawei Han",instituition)]

# def extract_information(p_url):
#     import requests
#     from bs4 import BeautifulSoup

#     headers = {
#     'Access-Control-Allow-Origin': '*',
#     'Access-Control-Allow-Methods': 'GET',
#     'Access-Control-Allow-Headers': 'Content-Type',
#     'Access-Control-Max-Age': '3600',
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
#     }

#     information_criteria = ["Education", "Biography","Professional Highlights", "Research Statement", "Honors"]
#     infoDictionary = {}

#     url = p_url
#     req = requests.get(url, headers)
#     soup = BeautifulSoup(req.content, 'html.parser')

#     for ic in information_criteria:
#         for heading in soup.find_all('h2'):
#             if not ic in heading.text: continue
#             info_packet = ""
#             for sib in heading.find_next_siblings():
#                 if sib.name == "h2":
#                     break
#                 else:
#                     #print(ic)
#                     info_packet+=" "+sib.text

#             if ic in infoDictionary:
#                 infoDictionary[ic]+= info_packet
#             else:
#                 infoDictionary[ic] = info_packet

#     print(infoDictionary['Research Statement'])
#     return infoDictionary

###############################################################
# html = open(test_url).read()
#     webUrl  =  urlopen(test_url)
#     print ("result code: " + str(webUrl.getcode()))

#     page_html =  webUrl.read()
#     h = html2text.HTML2Text()
#  # Ignore converting links from HTML
#     h.ignore_links = True
#     print(h.handle(page_html))
# print(page_html)
# print(html2text.html2text(page_html))

# resource = urlopen(test_url3)
# content = resource.read()
# #charset = resource
# content = content.decode('utf-8')

# ascii_page = html2text.html2text(content)
# print(ascii_page)
# print(ascii_page.find("##"))