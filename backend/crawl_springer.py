"""
This module crawls publication data from the springer knowledge base.

Knowledge Base Reference: https://dev.springernature.com/example-metadata-response 
"""

import requests
import pandas as pd
import json
api_key = "e04afc19febd3700b686b4afade1c7db"

def crawl(professor, university):
    """Crawls springer knowledge base for publications associated with the professor from the specified university.

    Args:
        professor (str): Name of professor
        university (str): Name of university

    Returns:
        publications (pandas dataframe): Data containing the publications' titles, authors, abstracts, and DOI's

    """
    # Initialization
    column_names = ["title", "authors", "abstract", "doi", "citations"]
    publications = pd.DataFrame(columns = column_names)
    response = requests.get("http://api.springernature.com/meta/v2/json?q=name:" + professor.replace(" ", "+") + "&api_key=" + api_key)
    metadata = json.loads(response.text)
    
    for pub in metadata['records']:
        # Check if the queried Professor is a creator of the publications in the API results
        temp_dict = {}
        if (check_creator(professor, pub['creators'])):
            temp_dict['title'] = pub['title']
            temp_dict['authors'] = creatorsListToString(pub['creators']) # Convert list creators to comma separated string
            temp_dict['abstract'] = pub['abstract']
            temp_dict['doi'] = pub['doi']
            temp_dict["citations"] = 0

        publications = publications.append(temp_dict, ignore_index=True)
        
    return publications

def check_creator(professor, creators):
    """Checks if the given professor is one of the creators of the publication.

    Args:
        professor (str): Name of professor
        creators (list): List of creators from Springer

    Returns:
        True (bool): Professor is one of the creators
        False (bool): Professor is not one of the creators

    """
    # Loop through the list of creators
    for x in range(len(creators)):
        name = creator_to_string(creators[x]["creator"])
        
        if (professor.lower() == name.lower()):   
           return True
    
    return False

def creator_to_string(creator_name):
    """Formats creator name to (First Name Last Name) format.

    Args:
        creator_name (str): Name of creator

    Returns:
        (str): creator name in (First Name Last Name) format

    """
    # Initialization
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

def creatorsListToString(creators_list):
    """Converts list of Springer creators into a comma separated string.

    Args:
        creators_list (list): List of creators from Springer

    Returns:
        temp (str): Comma separated string of all the creators

    """
    temp = ""
    
    for x in range(len(creators_list)):
        temp += creator_to_string(creators_list[x]["creator"])
        
        if (x != len(creators_list) - 1):
            temp += ", "

    return temp.strip()

# creators = [{ "creator":"Hughes, Caren L"},{ "creator":"Yorio, Jeffrey T"},{"creator":"Kovitz, Craig"},{"creator":"Oki, Yasuhiro"}]
# crawl("10.1007/BF00627098")
publications = crawl("Yoshua Bengio", "University of Montreal")
print(publications['authors'])
# check_creator("Caren L Hughes", creators)
# creatorsListToString(creators)

