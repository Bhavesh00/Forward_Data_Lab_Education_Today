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

def containsProfessor(authors_list, professor):
    # "authors": [{"name": "\u8d3a\u51e4\u971e", "id": "2404364408"}]"
    for x in authors_list:
        if "name" in x:
            if professor in x["name"]:
                return True
    
    return False

# authors_list = [{"name": "\u8d3a\u51e4\u971e", "id": "2404364408"}]
# containsProfessor(authors_list, "")

def authorsToString(authors_list):
    temp = ""
    for x in range(len(authors_list)):
        temp += authors_list[x]["name"]

        if (x != len(authors_list) - 1):
            temp += ", "
    return temp

def crawl(professor, university):
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)
    aminer = crawl_aminer(professor, university)
    mag = crawl_mag(professor, university)
    publications.append(aminer)
    publications.append(mag)

def crawl_aminer(professor, university):
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Open aminer files
    aminer_file_papers = open("backend/data/aminer_papers_12.txt", 'r')

    # Loop through Aminer file.
    while True:
        # Get next line from file
        line = aminer_file_papers.readline()
    
        # if line is empty end of file is reached
        if not line:
            break

        # Load the line into json
        pub_json = json.loads(line)
        tempDict = {}   

        # print(pub_json["authors"])
        if containsProfessor(pub_json["authors"], professor):
            # author.org (check if this contains query university)

            if "authors" in pub_json:
                tempDict["authors"] = authorsToString(pub_json["authors"])
            else:
                tempDict["authors"] = ""

            if "title" in pub_json:
                tempDict["title"] = pub_json["title"]
            else:
                tempDict["title"] = ""
            
            if "abstract" in pub_json:
                tempDict["abstract"] = pub_json["abstract"]
            else:
                tempDict["abstract"] = ""
            
            if "doi" in pub_json:
                # print(pub_json["doi"])
                tempDict["doi"] = pub_json["doi"]
            else:
                tempDict["doi"] = ""
            
            if "citations" in pub_json:
                tempDict["citations"] = pub_json["n_citation"]
            else:
                tempDict["citations"] = ""
            
            publications.append(tempDict, ignore_index="True")
            print(tempDict)
    
    return publications


def crawl_mag(professor, university):
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)

    # Open mag files
    mag_file_papers = open("backend/data/mag_papers_10.txt", 'r')

    # Loop through Aminer file.
    while True:
        # Get next line from file
        line = mag_file_papers.readline()
    
        # if line is empty end of file is reached
        if not line:
            break

        # Load the line into json
        pub_json = json.loads(line)
        tempDict = {}   

        # print(pub_json["authors"])
        if containsProfessor(pub_json["authors"], professor):
            # author.org (check if this contains query university)

            if "authors" in pub_json:
                tempDict["authors"] = authorsToString(pub_json["authors"])
            else:
                tempDict["authors"] = ""

            if "title" in pub_json:
                tempDict["title"] = pub_json["title"]
            else:
                tempDict["title"] = ""
            
            if "abstract" in pub_json:
                tempDict["abstract"] = pub_json["abstract"]
            else:
                tempDict["abstract"] = ""
            
            if "doi" in pub_json:
                # print(pub_json["doi"])
                tempDict["doi"] = pub_json["doi"]
            else:
                tempDict["doi"] = ""
            
            if "citations" in pub_json:
                tempDict["citations"] = pub_json["n_citation"]
            else:
                tempDict["citations"] = ""
            
            publications.append(tempDict, ignore_index="True")
            print(tempDict)

    return publications


# crawl_aminer("carolina galais", "")
# crawl_mag("A. Hrynkiewicz", "")