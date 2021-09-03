""" 
This program extracts professor and publication data from Microsoft Open Academic Graph (OAG) Knowledge Base.
""" 

from googlesearch import search
import requests
from bs4 import BeautifulSoup as bs
import html2text
import io
import sys
import json
from getpass import getpass
from mysql.connector import connect, Error
import pandas as pd

def contains_professor(authors_list, professor):
    """Checks if the given professor is one of the authors of the publication.

    Args:
        authors_list (list): List of authors from OAG
        professor (str): Name of professor

    Returns:
        True (bool): Professor is one of the authors
        False (bool): Professor is not one of the authors

    """

    for x in authors_list: # authors_list example: "authors": [{"name": "\u8d3a\u51e4\u971e", "id": "2404364408"}]"
        if "name" in x:
            if professor.lower() in x["name"].lower():
                return True
    
    return False

def authors_to_string(authors_list):
    """Converts list of OAG authors into a comma separated string.

    Args:
        authors_list (list): List of authors from OAG

    Returns:
        temp (str): Comma separated string of all the creators

    """
    temp = ""
    for x in range(len(authors_list)):
        temp += authors_list[x]["name"]

        if (x != len(authors_list) - 1):
            temp += ", "
    return temp

def crawl(professor, university):
    """Crawls OAG knowledge base for publications associated with the professor from the specified university.

    Args:
        professor (str): Name of professor
        university (str): Name of university

    Returns:
        publications (pandas dataframe): Data containing the publications' titles, authors, abstracts, and DOI's

    """
    # Initialization
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Call crawling helper functions
    aminer = crawl_helper(professor, university, "data/aminer_papers_12.txt")
    mag = crawl_helper(professor, university, "data/mag_papers_10.txt",)
    publications = publications.append(aminer)
    publications = publications.append(mag)
    return publications

def crawl_helper(professor, university, file):
    """Crawler helper function that crawls data for publications associated with the professor from the specified university.

    Args:
        professor (str): Name of professor
        university (str): Name of university
        file (str): Path of file

    Returns:
        publications (pandas dataframe): Data containing the publications' titles, authors, abstracts, and DOI's

    """
    # Initialization
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Open file
    file_papers = open(file, 'r')

    # Loop through file.
    while True:
        # Get next line from file
        line = file_papers.readline()
    
        # If line is empty end of file is reached
        if not line:
            break

        # Load the line into json
        pub_json = json.loads(line)
        temp_dict = {}   

        if contains_professor(pub_json["authors"], professor):
            # TODO: author.org (check if this contains query university)

            if "authors" in pub_json:
                temp_dict["authors"] = authors_to_string(pub_json["authors"])
            else:
                temp_dict["authors"] = ""

            if "title" in pub_json:
                temp_dict["title"] = pub_json["title"]
            else:
                temp_dict["title"] = ""
            
            if "abstract" in pub_json:
                temp_dict["abstract"] = pub_json["abstract"]
            else:
                temp_dict["abstract"] = ""
            
            if "doi" in pub_json:
                # print(pub_json["doi"])
                temp_dict["doi"] = pub_json["doi"]
            else:
                temp_dict["doi"] = ""
            
            if "citations" in pub_json:
                temp_dict["citations"] = pub_json["n_citation"]
            else:
                temp_dict["citations"] = ""
            
            publications = publications.append(temp_dict, ignore_index=True)
            # print(temp_dict)
    
    return publications

def test_OAG():
    """Testing suite for OAG crawler"""
    publications = crawl_helper("Juan Jacobo", "University of Colorado Boulder", "data/oag_test.txt")
    assert "El concepto de empresa internacional en la regulación de los contratos de arrendamiento de inmuebles" in publications.values
    assert "Juan Jacobo" in publications.values

    publicationsTwo = crawl_helper("Mark C. Hakey", "University of New Hampshire Durham", "data/oag_test.txt")
    assert "Frequency doubling hybrid photoresist having negative and positive tone components and method of preparing the same" in publicationsTwo.values
    assert "Mark C. Hakey, Steven J. Holmes, David V. Horak, Ahmad D. Katnani, Niranjan M. Patel, Paul A. Rabidoux" in publicationsTwo.values

    print("All OAG Crawler tests passed.")

# test_OAG()