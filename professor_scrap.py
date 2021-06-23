from googlesearch import search # https://pypi.org/project/googlesearch-python/
import pandas as pd

'''
Go to Google. 
Search (name,institution). 
Filter results --> URLs that are faculty homepages.
'''
# to search
professor_name = "Kevin Chen-Chuan Chang"
instituition = "UIUC"

# query = professor_name + " " + instituition
  
# for j in search(query, lang="en", num_results=5):
#     print(j)


prof_list = [(professor_name,instituition),("Jiawei Han",instituition)]

def query_urls(prof_list):
    
    for p_name, p_instituition in prof_list:
        query = p_name + " " + p_instituition

        print (search(query, lang="en", num_results=10))
        print ("\n")


'''
Go through each page. 
Extract information: 
    -Biography
    -Education
    -Awards
    -Research interests
    -Publications
'''

def extract_information(p_url):
    information_criteria = ["Biography", "Education","Awards", "Research interests", "Publications"]






def main():
    query_urls(prof_list)

if __name__ == "__main__":
    main()