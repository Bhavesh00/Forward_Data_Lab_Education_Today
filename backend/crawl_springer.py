"""
This module crawls publication data from the springer knowledge base.

Knowledge Base Reference: https://dev.springernature.com/example-metadata-response 
"""
import requests
import pandas as pd
import json
api_key = "e04afc19febd3700b686b4afade1c7db"

# This function takes in the name of a professor and a university.
# Returns a dataframe containing the publication title, publication authors, publication abstract, and publication DOI 
# of the publications associated with the professor from the given university.
def crawl(professor, university):
    column_names = ["title", "authors", "abstract", "doi"]
    publications = pd.DataFrame(columns = column_names)
    response = requests.get("http://api.springernature.com/meta/v2/json?q=name:" + professor.replace(" ", "+") + "&api_key=" + api_key)
    metadata = json.loads(response.text)
    
    for pub in metadata['records']:
        tempDict = {}
        # Check if the queried Professor is actually a creator of the publications in the API results
        if (checkCreator(professor, pub['creators'])):
            tempDict['title'] = pub['title']
            tempDict['authors'] = creatorsListToString(pub['creators']) # Convert list creators to comma separated string
            tempDict['abstract'] = pub['abstract']
            tempDict['doi'] = pub['doi']

        publications = publications.append(tempDict, ignore_index=True)
        
    return publications

# This function takes in the professor and a list of creators given by Springer, and checks if the professor is one of the creators
# of the publication and returns true. Returns false if the professor is not a creator.
def checkCreator(professor, creators):
    for x in range(len(creators)):
        name = creatorToString(creators[x]["creator"])
        
        if (professor == name):   
           return True
    
    return False

# This function takes in a single creator name and formats it so that it is in (First Name Last Name) format.
def creatorToString(creator_name):
    name = creator_name.split(" ")
    first_name = ""
    middle_name = ""
    last_name = ""

    if (len(name) == 2):  # Handle case where there is no middle name
        last_name = name[0][:-1]
        first_name = name[1]

    elif(len(name) == 3): # Handle case where there is a middle name
        last_name = name[0][:-1]
        first_name = name[1]
        middle_name = name[2] + ' '

    return first_name + ' ' + middle_name + last_name

# This function takes in a list of creators given by Springer, and returns a comma separated string of all the creators.
def creatorsListToString(creators_list):
    temp = ""
    
    for x in range(len(creators_list)):
        temp += creatorToString(creators_list[x]["creator"])
        
        if (x != len(creators_list) - 1):
            temp += ", "

    return temp.strip()



# creators = [{ "creator":"Hughes, Caren L"},{ "creator":"Yorio, Jeffrey T"},{"creator":"Kovitz, Craig"},{"creator":"Oki, Yasuhiro"}]
# crawl("10.1007/BF00627098")
# publications = crawl("Yoshua Bengio", "University of Montreal")
# print(publications['authors'])
# checkCreator("Caren L Hughes", creators)
# creatorsListToString(creators)

