"""
This module crawls publication and professor data from the arXiv knowledge base.

Knowledge Base Reference: https://www.kaggle.com/Cornell-University/arxiv
"""

import pandas as pd
import json
from collections import Counter, defaultdict

def get_metadata():
    """This function returns the data from the json file."""
    with open('data/arxiv-metadata-oai-snapshot.json') as f:
        for line in f:
            yield line

def crawl(professor, university):
    """Crawls Arxiv knowledge base for publications associated with the professor from the specified university.

    Args:
        professor (str): Name of professor
        university (str): Name of university

    Returns:
        publications (pandas dataframe): Data containing the publications' titles, authors, abstracts, and DOI's

    """

    # Initialization
    metadata = get_metadata()
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Loop through Arxiv data
    for ind, paper in enumerate(metadata):
        paper = json.loads(paper)
        temp_dict = {}

        # Check if professor names match
        if professor.lower() == paper['submitter'].lower():
            temp_dict['title'] = paper['title']
            temp_dict['authors'] = paper['authors']
            temp_dict['abstract'] = paper['abstract']
            temp_dict['doi'] = paper['doi']
        
        publications = publications.append(temp_dict, ignore_index=True)
    
    return publications

def ab_name_format(professor):
    """Formats professor name intto (First Initial, Middle Initial, Last Name) format.

    Args:
        professor (str): Name of professor

    Returns:
        (str): Professor name in (First Initial, Middle Initial, Last Name) format

    """
    if (professor == ""):
        return ""

    list = professor.split()
    temp = ""

    for i in range(len(list) - 1):
        s = list[i]
          
        # Adds the capital first character 
        temp += (s[0].upper()+'. ')
          
    temp += list[-1].title()
      
    return temp.strip()


crawl("", "")
# print(ab_name_format("Peter A Stuart"))
# crawl("Jiawei Han", "University of Illinois at Urbana-Champaign")