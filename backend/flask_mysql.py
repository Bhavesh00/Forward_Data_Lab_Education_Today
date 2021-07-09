from flask_route import app, mysql
from relation_graph import Graph
import professor_scrap
import filter_sites
import extract_keywords


def get_professor_ranked_list(professor_name, institution_name):
    cur = mysql.connection.cursor()
    query = "SELECT *\
            FROM Keywords \
            ORDER BY name and institution"
    cur.execute(query)
    fetch_data = cur.fetchall()
    cur.close()

    prof_dict = {}
    for column in fetch_data:
        name = column[0]
        institution = column[1]
        keyword = column[2]
        occurrence = column[3]
        dict_key = (name, institution)

        if dict_key not in prof_dict.keys():
            prof_dict[dict_key] = {}
        prof_dict[dict_key][keyword] = occurrence

    print(prof_dict)

    relation_graph = Graph()
    for key in prof_dict.keys():
        print(key, prof_dict[key])
        relation_graph.add_professor_node(key, prof_dict[key])
    ranked_list = relation_graph.related_professors((professor_name, institution_name))

    return_list = [node[0] for node in ranked_list]
    return return_list


def get_professor_info(professor_name, institution_name):
    cur = mysql.connection.cursor()
    query = "SELECT *\
            FROM Professor\
            WHERE name = %s and institution = %s"
    val = (professor_name, institution_name)

    cur.execute(query, val)
    fetch_data = cur.fetchall()
    cur.close()
    return fetch_data


def get_professor_publications(professor_name, institution_name):
    cur = mysql.connection.cursor()
    query = "SELECT *\
            FROM Publication\
            WHERE name = %s and institution = %s"
    val = (professor_name, institution_name)

    cur.execute(query, val)
    fetch_data = cur.fetchall()
    cur.close()
    return [[paper[0], paper[3]] for paper in fetch_data]


def scrape_professor_info(professor_name, institution_name):
    temp_list = [(professor_name, institution_name)]
    extracted_professors = professor_scrap.audit_professors(temp_list)
    professor_scrap.update_Professors_DB(extracted_professors)

    search_query = professor_name + ", " + institution_name

    urls = filter_sites.getPublicationUrlAndTitle(search_query)

    print(urls)
    extract_keywords.extract_process(professor_name, institution_name, urls)
    return
