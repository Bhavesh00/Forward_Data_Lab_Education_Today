from googlesearch import search

def homepage_finder(query):
    professor_name, institution = query
    search_query = professor_name+ ", "+ institution
    
    temp_list = search(search_query, 10, "en")
    professor_urls = []

    for url in temp_list:
        # Skip all search results of wikipedia and google scholar
        if "wikipedia" in url or "scholar.google" in url:
            continue
        # Only pick reputable sources; choose .edu or .org webpages
        if ".edu" in url or ".org" in url:
            professor_urls.append(url)
        # Return once upper limit of 3 useable urls are found
        if len(professor_urls) == 3:
            break
    return professor_urls