"""
Knowledge Base Reference: https://www.kaggle.com/Cornell-University/arxiv

This module crawls publication and professor data from the arXiv knowledge base.
"""

import pandas as pd
import json
from collections import Counter, defaultdict

def get_metadata():
    # Make Relative Paths (https://stackoverflow.com/questions/918154/relative-paths-in-python)
    with open('/Users/bhavesh/Forward_Data_Lab_Education_Today/data/arxiv-metadata-oai-snapshot.json') as f:
        for line in f:
            yield line

# This function takes in the name of a professor and a university.
# This function returns a dataframe containing the publication title, publication authors, publication abstract, and publication DOI 
# of the publications associated with the professor from the given university.
def crawl(professor, university):
    # DataFrame
    metadata = get_metadata()
    column_names = ["title", "authors", "abstract", "doi"]
    publications = pd.DataFrame(columns = column_names)

    for ind, paper in enumerate(metadata):
        paper = json.loads(paper)
        tempDict = {}
        if professor == paper['submitter'] or abNameFormat(professor) in paper['authors']:
            tempDict['title'] = paper['title']
            tempDict['authors'] = paper['authors']
            tempDict['abstract'] = paper['abstract']
            tempDict['doi'] = paper['doi']

            """
            print(paper['title'])
            print(paper['authors'])
            print(paper['abstract'])
            print(paper['doi'])
            """
         
        publications = publications.append(tempDict, ignore_index=True)
    
    return publications


# This function converts the professor name (First Name Last Name) into (First Initial, Middle Initial, Last Name format) 
# and returns this string. This function will be used to match the author name formatting in the arXiv dataset.
def abNameFormat(professor):
    list = professor.split()
    temp = ""

    for i in range(len(list) - 1):
        s = list[i]
          
        # Adds the capital first character 
        temp += (s[0].upper()+'. ')
          
    temp += list[-1].title()
      
    return temp.strip()

# crawl("", "")
# print(abNameFormat("Peter A Stuart"))