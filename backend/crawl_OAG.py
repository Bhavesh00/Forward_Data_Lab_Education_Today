# This program extracts professor and publication data from Microsoft Open Academic Graph (OAG) Knowledge Base.

from googlesearch import search
import requests
from bs4 import BeautifulSoup as bs
import html2text
import io
import sys
import json
from getpass import getpass
from mysql.connector import connect, Error


# Push the publications individually to the publications table on MySQL
# search_query is in the format (professor, university)
def getPublicationAuthorAndTitle(search_query):

    # Initialization
    publications = []
    publications_titles = []
    keywords = {} # Dictionary that has publication title as key and keywords as the value
    professor = search_query.split(", ")[0]
    institution = search_query.split(", ")[1]
    urls = []

    # Open aminer papers
    aminer_file_authors  = open("aminer_authors.txt")
    aminer_file_papers  = open(aminer_papers.txt)

    aminer_data_authors = json.load(aminer_file_authors)
    aminer_data_papers = json.load(aminer_file_papers)
    
    for x in aminer_data_papers:
        if not x["title"]  in publications_titles:
            publications_titles.append(x["title"])
            urls.append(x['url'][0]) # Check if exists to avoid potential error.
            keywords[x["titles"]] = x["keywords"]


    # Open mag papers 
    mag_file_authors  = open(mag_authors.txt)
    mag_file_papers  = open(mag_papers.txt)

    for x in mag_data_papers:
        if not x["title"]  in publications_titles:
            publications_titles.append(x["title"])
            urls.append(x['url'][0]) # Check if exists to avoid potential error.
            keywords[x["titles"]] = x["keywords"]

    try:
        with connect(
                host="35.225.165.28",
                user="root",
                password="gB4zpufPpuvK7yEf",
                database='fwddata'

        ) as connection:
            mycursor = connection.cursor()
            sql = "INSERT IGNORE INTO Publication (title, name, institution, url) VALUES (%s, %s, %s, %s)"

            for x in range(len(publications)):
                val = (publications_titles[x], professor, institution, publications[x])
                mycursor.execute(sql, val)

            connection.commit()
            connection.close()

    except Error as e:
        print(e)

    return publications