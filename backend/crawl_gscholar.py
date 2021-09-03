""" 
This program extracts professor and publication data from Google Scholar. 

Knowledge base reference: https://scholar.google.com/ 

WARNING: WEB SCRAPING CODE CAN BREAK IN THIS MODULE DUE TO VOLATILE GOOGLE SCHOLAR HTML TAGS THAT CHANGE BETWEEN UPDATES.
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

def crawl(professor, university):
    """Crawls Google Scholar knowledge base for publications associated with the professor from the specified university.

    Args:
        professor (str): Name of professor
        university (str): Name of university

    Returns:
        publications (pandas dataframe): Data containing the publications' titles, authors, abstracts, and DOI's

    """

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
    publications_citations = []
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
            print(soup.text)
            for link in soup.find_all(["a"], "gsc_a_at"):
                # Potential Error as the tag changes to data-href on some browsers:
                if link.get('href') is not None:
                    publications_urls.append("https://scholar.google.com" + link.get('href'))
    
    # TODO: Need to still handle case where an author's publication list spans multiple pages on Google Scholar
    # Need to also add proxy to avoid Google bot detection.
    for url in publications_urls:
        # Accessing the Webpage
        page = requests.get(url)

        # Getting the webpage's content in pure html
        soup = bs(page.content, features="lxml")
    
        # Get Publication Title
        title = soup.find(["a"], "gsc_oci_title_link")
        print(title.text)
        publications_titles.append(title.text)
        print(len(publications_titles))

        # Get Publication Authors
        authors = soup.find(class_="gsc_oci_value")
        publications_authors.append(authors.text)

        # Get Publication Abstracts
        abstract = soup.find(class_="gsh_small")
        publications_abstracts.append(abstract.text)

        # Get Number of Citations
        num_citations = soup.find(class_="gsc_a_c")
        publications_citations.append(num_citations.text)

    # Add the publications
    for x in range(len(publications_titles)):
        temp_dict = {}
        temp_dict['title'] = publications_titles[x]
        temp_dict['authors'] = publications_authors[x]
        temp_dict['abstract'] = publications_abstracts[x]
        temp_dict['doi'] = ""
        temp_dict['citations'] = publications_citations[x]
        publications = publications.append(temp_dict, ignore_index=True)

    return publications

def test_gscholar():
    """Testing suite for Google Scholar crawler"""
    publications = crawl("Jiawei Han", "University of Illinois at Urbana-Champaign")
    assert "Data mining: concepts and techniques" in publications.values
    assert "Mining frequent patterns without candidate generation: A frequent-pattern tree approach" in publications.values

    publicationsTwo = crawl("Gul Agha", "University of Illinois at Urbana-Champaign")
    assert "CUTE: A concolic unit testing engine for C" in publicationsTwo.values
    assert "Concurrent object-oriented programming" in publicationsTwo.values

    print("All Google Scholar Crawler tests passed.")
    
# test_gscholar()
