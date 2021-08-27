""" 
This program extracts professor and publication data from Google Scholar. https://scholar.google.com/  
"""

from googlesearch import search
import requests
from bs4 import BeautifulSoup as bs
import html2text
import io
import sys
import pandas as pd
import json
from getpass import getpass
from mysql.connector import connect, Error
import time


# This function takes in the name of a professor and a university.
# Returns a dataframe containing the publication title, publication authors, publication abstract, and publication DOI 
# of the publications associated with the professor from the given university.
def crawl(professor, university):
    # Reconfigure the encoding to avoid issues
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    # Initialization
    search_query = professor + ", " + university
    list = search(search_query, 10, "en") # Google search results
    google_urls = []
    publications_urls = []
    publications_titles = []
    publications_authors = []
    publications_abstracts = []
    publication_citations = []

    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Finding List of Google search URL's that have .org, .edu, or scholar.google in the URL
    for i in range(len(list)):
        if ".edu" in list[i] or ".org" in list[i] or "scholar.google" in list[i]:
            google_urls.append(list[i])

    # Loop through google search URL's
    for url in google_urls:
        # Accessing the Webpage
        page = requests.get(url)

        # Getting the webpage's content in pure html
        soup = bs(page.content, features="lxml")

        # Extracting Abstract Links from Google Scholar
        if "scholar.google" in url:
            print("Google Scholar Publication: " + url)
            for link in soup.find_all(["a"], "gsc_a_at"):
                # Potential Error as the tag changes to data-href on some browsers:
                # print(link.get('data-href'))
                if link.get('href') is not None:
                    publications_urls.append("https://scholar.google.com" + link.get('href'))
                    # publications_titles.append(link.text)

    print(publications_urls)
    
    # TODO: Need to still handle case where an author's publication list spans multiple pages on Google Scholar
    for url in publications_urls:
        # Accessing the Webpage
        page = requests.get(url)

        print("accessed")

        # Getting the webpage's content in pure html
        soup = bs(page.content, features="lxml")
    
        # Get Publication Title
        title = soup.find(["a"], "gsc_oci_title_link")
        print(title.text)
        publications_titles.append(title.text)
        print(len(publications_titles))

        # Get Publication Authors
        # authors = 
        # publications_authors


        # Get Publication Abstracts
        # abstract = soup.find_all(class_="gsh_small")
        # print(abstract)
        # publications_abstracts

        # Get Number of Citations
        # num_citations = 
        # publications_citations



    return


# search_query = "Jiawei Han, University of Illinois at Urbana-Champaign"
crawl("Jiawei Han", "University of Illinois at Urbana-Champaign")
