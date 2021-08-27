from googlesearch import search
import requests
from bs4 import BeautifulSoup as bs
import html2text
import io
import sys
import json
from getpass import getpass
from mysql.connector import connect, Error


# This function converts the HTML of the professor pages into local text files for analysis
def htmlToText(search_query):
    # Reconfigure the encoding to avoid issues
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    # Initialization
    list = search(search_query, 10, "en")
    urls = []

    # Finding List of Google search URL's that have .org, .edu, or scholar.google in the URL
    for i in range(len(list)):
        if ".edu" in list[i] or ".org" in list[i] or "scholar.google" in list[i]:
            urls.append(list[i])
    # print(urls)

    # Converting the HTML content for each page into separate text files
    count = 0
    for url in urls:
        # Accessing the Webpage
        page = requests.get(url)

        # Getting the webpage's content in pure html
        soup = bs(page.content, features="lxml")

        # Convert HTML into easy-to-read plain ASCII text
        clean_html = html2text.html2text(soup.prettify())
        file_name = "site" + str(count) + ".txt"
        count += 1
        with io.open(file_name, "w", encoding="utf-8") as temp_file:
            temp_file.write(clean_html)
            temp_file.close()


# This function returns the publications' URL and Title as JSON strings. It also INSERTS the data into the database.
def getPublicationUrlAndTitle(search_query):
    # Reconfigure the encoding to avoid issues
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    # Initialization
    list = search(search_query, 10, "en")
    urls = []
    publications = []
    publications_titles = []
    professor = search_query.split(", ")[0]
    institution = search_query.split(", ")[1]

    # Finding List of Google search URL's that have .org, .edu, or scholar.google in the URL
    for i in range(len(list)):
        if ".edu" in list[i] or ".org" in list[i] or "scholar.google" in list[i]:
            urls.append(list[i])
    # print(urls)

    # Converting the HTML content for each page into separate text files
    count = 0
    for url in urls:
        # Accessing the Webpage
        page = requests.get(url)

        # Getting the webpage's content in pure html
        soup = bs(page.content, features="lxml")

        # Extracting Abstract Link from Google Scholar
        if "scholar.google" in url:
            print("Google Scholar Publication: " + url)
            for link in soup.find_all(["a"], "gsc_a_at"):
                # Potential Error as the tag changes to data-href on some browsers:
                # print(link.get('data-href'))
                if link.get('href') is not None:
                    publications.append("https://scholar.google.com" + link.get('href'))
                    publications_titles.append(link.text)

    # Convert Python arrays to JSON strings
    # jsonStrUrls = json.dumps(publications)
    # print(jsonStrUrls)
    # jsonStrPublicationTitles = json.dumps(publications_titles)
    # print(publications_titles)

    # Print out the publication titles and url's for the professor.
    # for x in range(len(publications)):
    #     print(publications_titles[x])
    #     print(publications[x])

    # Push the publications individually to the publications table on MySQL
    try:
        with connect(
                host="104.198.163.126",
                user="root",
                password="yEBpALG6zHDoCFLn",
                database='project'

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


# search_query = "Jiawei Han, University of Illinois at Urbana-Champaign"
# # htmlToText(search_query)
# getPublicationUrlAndTitle(search_query)
