"""
This module works very closely with the Distributed Crawler Management Module (in fact, you could 
consider them acting as a singular module)  to aggregate information from scraping tasks and from 
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

# Takes in professor, university
# Handles overlaps from the different data sets
# Handles conflict information
# Returns publication data and professor information
def consolidate(professor, university):
    # Add Edit Distance Function based on titles
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)
    arxiv_publications = arxiv.crawl(professor, university)
    springer_publications = springer.crawl(professor, university)
    # gscholar_publications = gscholar.crawl(professor, university)
    # oag_publications = oag.crawl(professor, university)

    publications.append(arxiv_publications)
    publications.append(springer_publications)
    # publications.append(gscholar_publications)
    # publications.append(oag_publications)
    

    return publications

publications = consolidate("Jiawei Han", "University of Illinois at Urbana-Champaign")
print(publications)


publications = consolidate("Yoshua Bengio", "University of Montreal")
print(publications)