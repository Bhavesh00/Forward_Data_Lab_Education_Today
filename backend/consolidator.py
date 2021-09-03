"""
This module works very closely with the Distributed Crawler Management Module (in fact, you could 
consider them acting as a singular module) to aggregate information from scraping tasks and from 
existing knowledge bases (e.g. MAG, OAG) into a unified database for the EducationToday website.  

Note that this module does not handle ranking or keyword assignment related data. It only handles 
core data: descriptive data of each entity (e.g. research position of an author, number of citations 
for a publication) and core linking relations between each entity (e.g. current institution of professors).
"""

import crawl_gscholar as gscholar
import crawl_OAG as oag
import crawl_arxiv as arxiv
import crawl_springer as springer
import pandas as pd
import json

def consolidate(professor, university):
    """Handles overlaps and conflicting informatino from the different knowledge bases.

    Args:
        professor (str): Name of professor
        university (str): Name of university

    Returns:
        publications (pandas dataframe): Data containing the publications' titles, authors, abstracts, and DOI's

    """
    # Add Edit Distance Function based on titles to remove duplicates. Utilize 
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Crawl Arxiv
    arxiv_publications = arxiv.crawl(professor, university)
    print("Arxiv crawling complete")
    print(arxiv_publications)

    # Crawl Springer
    springer_publications = springer.crawl(professor, university)
    print("Springer crawling complete")
    print(springer_publications)

    # Crawl MAG
    mag_publications = oag.crawl_mag(professor, university)
    print("MAG crawling complete")
    print(mag_publications)

    # Crawl Aminer
    aminer_publications = oag.crawl_aminer(professor, university)
    print("Aminer crawling complete")
    print(aminer_publications)

    # Crawl Google Scholar
    # gscholar_publications = gscholar.crawl(professor, university)
    # print("Google Scholar crawling complete")
    # print(gscholar_publications)
    
    publications = publications.append(arxiv_publications)
    publications = publications.append(springer_publications)
    publications = publications.append(mag_publications)
    publications = publications.append(aminer_publications)
    # publications = publications.append(gscholar_publications)
    
    return publications

def remove_duplicates(publications):
    """Removes duplicate entries in the publication dataframe based on DOI #'s and title names.

    Args:
        publications (pandas dataframe): Publications data

    Returns:
        publications (pandas dataframe): Data containing the publications' titles, authors, abstracts, and DOI's

    """
    publications = publications.drop_duplicates(subset=['title'])
    publications = publications.drop_duplicates(subset=['doi']) # Might potentially need to handle empty DOI's.
    return publications

def test_consolidator():
    """Testing suite for consolidator"""
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Testing removing duplicates based on DOI #.
    temp_dict = {}   
    temp_dict['title'] = "A Comparative Study of Learning Outcomes for Online Learning Platforms"
    temp_dict['authors'] = "Yoshua Bengio"
    temp_dict['abstract'] = "Abstract information"
    temp_dict['doi'] = "10.1007/978-3-030-78270-2_59"
    temp_dict["citations"] = 0
    publications = publications.append(temp_dict, ignore_index=True)
    temp_dict['title'] = "A Comparative Study"
    publications = publications.append(temp_dict, ignore_index=True)
    publications = remove_duplicates(publications)
    assert len(publications) == 1

    # Testing removing duplicates based on Title
    temp_dict['doi'] =  "10.1007/978-2-031-72340-3_61"
    temp_dict['title'] = "A Comparative Study of Learning Outcomes for Online Learning Platforms"
    publications = publications.append(temp_dict, ignore_index=True)
    publications = remove_duplicates(publications)
    assert len(publications) == 1
    print("All consolidator tests passed.")

# test_consolidator()