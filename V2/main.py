from Homepage_Finding.homepage_finder import homepage_finder
from Homepage_Extraction.homepage_extractor import extract_homepage
import pprint

def search_professor(prof_tuple):
    data_store = []
    # Module 1
    professor_page_list = homepage_finder(prof_tuple)
    print(professor_page_list, "\n")
    # Module 2
    for url in professor_page_list:
        data_store.append(extract_homepage(url))
    # Module 3

    return data_store

if __name__ == '__main__':
    test_tup = ("Kevin Chenchuan Chang", "University of Illinois Urbana-Champaign")
    data_store = search_professor(test_tup)

    for dic in data_store:
        pprint.pprint(dic)
        print("---------------WEBSITE END-----------------")