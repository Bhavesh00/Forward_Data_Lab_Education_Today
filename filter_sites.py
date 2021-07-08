from googlesearch import search
import requests 
from bs4 import BeautifulSoup as bs
import html2text
import io
import sys
import json

# Reconfigure the encoding to avoid issues
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


# Initialization
search_query = "Jiawei Han, University of Illinois at Urbana-Champaign"
list = search(search_query, 10, "en")
urls = []
publications = []

# Finding List of Google search URL's that have .org, .edu, or scholar.google in the URL
for i in range(len(list)):
    if ".edu" in list[i] or ".org" in list[i] or "scholar.google" in list[i]:
        urls.append(list[i])
print(urls)

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
            # print(link.get('data-href'))
            publications.append("https://scholar.google.com" + link.get('data-href'))

    # Convert HTML into easy-to-read plain ASCII text
    clean_html = html2text.html2text(soup.prettify())
    file_name = "site" + str(count) + ".txt"
    count += 1
    with io.open(file_name, "w", encoding="utf-8") as temp_file:
        temp_file.write(clean_html)
        temp_file.close()

# Convert Python array to JSON array
jsonStr = json.dumps(publications)
print(jsonStr)

# Print out the publications for the professor.
for x in range(len(publications)):
   print(publications[x])