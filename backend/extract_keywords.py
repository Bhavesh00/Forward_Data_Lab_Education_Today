import os
import requests
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from bs4 import BeautifulSoup
import nltk
# nltk.download()
import yake
import mysql.connector

# [1] has built-in keywords
normal_pdf_urls = ["https://www.researchgate.net/profile/Abdussalam_Alawini/publication"
                   "/325090722_Provenance_Analysis_for_Missing_Answers_and_Integrity_Repairs/links"
                   "/5af5aaec0f7e9b026bceafec/Provenance-Analysis-for-Missing-Answers-and-Integrity-Repairs.pdf",
                   "https://educationaldatamining.org/files/conferences/EDM2020/papers/paper_150.pdf",
                   "http://sites.computer.org/debull/A18mar/p27.pdf",
                   "http://sites.computer.org/debull/A18mar/p39.pdf"]

test_pdf_urls = ["https://drive.google.com/file/d/1iYsVVlMo57OENah9tc0oNJaBV02jcMqc",
                 "https://drive.google.com/file/d/1i2FWf2DwYtOsTTj79dm9ujnago4PB9Io",
                 "https://drive.google.com/file/d/1DGLaDupsKVvL04-8mdOHKxycyy114Hnj",
                 "https://drive.google.com/file/d/1hYaDnM0NnTi8kOh41jr1aUaBkZMzmvII",
                 "https://drive.google.com/file/d/1FqU_tpl_xBvLmRAcyMbTqfoWEctILO--",
                 "https://drive.google.com/file/d/1Ny9DiliMHxH_ik5VPWHwYE7zU7AkVwbD",
                 "https://drive.google.com/file/d/1BgrprdFbOEpq4MkHdm685Rdd63wlC3qw",
                 "https://drive.google.com/file/d/1eJ6bkh2kjVjxho-3u4ei4rDyQSqZRxZD",
                 "https://drive.google.com/file/d/1kzACi2rPnylLe0j5h_RpbWjApSO4VHi7",
                 "https://drive.google.com/file/d/13MThXy8DXhlx3bgrbHKDIzdc8dfvMfJu",
                 "https://drive.google.com/file/d/1BDFW4dYUxS3O_QHqqmQmSSagJy6Jmf1P",
                 "https://drive.google.com/file/d/140y2UaYncRE9vLBMDdpccn9yp_dw9Etq",
                 "https://drive.google.com/file/d/1yBf-WuRKbNJWNeF2M-EGleYrxXiQycuf"]

test_google_scholar_urls = [
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:69ZgNCALVd0C",
    "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:u5HHmVD_uO8C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:kRWSkSYxWN8C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:eQOLeE2rZwMC",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:d1gkVwhDpl0C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:u-x6o8ySG0sC",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:_B80troHkn4C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:WF5omc3nYNoC",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:9yKSN-GCB0IC",
    # "/citations?view_op=view_citation&hl=en&oe=ASCII&user=Kv9AbjMAAAAJ&citation_for_view=Kv9AbjMAAAAJ:31TvLzYri2IC"
]

google_scholar_prefix = "https://scholar.google.com"

local_filename = "download.pdf"


def extract_keywords_from_pdf():
    pdf_string = convert_pdf_to_str()

    language = "en"
    max_ngram_size = 2
    deduplication_threshold = 0.9
    num_keywords = 8
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=num_keywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(pdf_string)
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)

    keywords = [keyword[0].lower() for keyword in keywords]
    keywords = sorted(keywords, key=len)

    keywords_no_repeat = []
    for keyword in keywords:
        if keyword not in keywords_no_repeat:
            if keyword[-1] == 's':
                if keyword[:-1] in keywords_no_repeat:
                    continue
            elif keyword[-2:-1] == 'es':
                if keyword[:-2] in keywords_no_repeat:
                    continue
            keywords_no_repeat.append(keyword)
    return keywords_no_repeat


def convert_pdf_to_str():
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    device = TextConverter(resource_manager, return_string, codec='utf-8', laparams=LAParams())
    file = open(local_filename, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, device)
    for page in PDFPage.get_pages(file, set(), maxpages=0, password="", caching=True, check_extractable=True):
        interpreter.process_page(page)
    file.close()
    device.close()
    pdf_string = return_string.getvalue()
    return_string.close()
    return pdf_string


def download_pdf_from_url(url: str):
    if "drive.google" in url:
        download_pdf_from_google_drive_url(url)
        return
    download_pdf_from_normal_url(url)


def download_pdf_from_normal_url(url: str):
    response = requests.get(url, stream=True)
    with open(local_filename, 'wb') as file:
        file.write(response.content)


def download_pdf_from_google_drive_url(url: str):
    file_id = url.split('/')[5]
    url = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(url, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, local_filename)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    chunk_size = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)


def scrape_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find('div', class_="gsh_csp")
    if container is None:
        print(response.content)
        return soup.find('div', class_="gsh_small").text
    return container.text


def extract_keywords_from_description(description):
    language = "en"
    max_ngram_size = 2
    deduplication_threshold = 0.9
    num_keywords = 8
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=num_keywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(description)
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)

    keywords = [keyword[0].lower() for keyword in keywords]
    keywords = sorted(keywords, key=len)

    keywords_no_repeat = []
    for keyword in keywords:
        if keyword not in keywords_no_repeat:
            if keyword[-1] == 's':
                if keyword[:-1] in keywords_no_repeat:
                    continue
            elif keyword[-2:-1] == 'es':
                if keyword[:-2] in keywords_no_repeat:
                    continue
            keywords_no_repeat.append(keyword)
    return keywords_no_repeat


def update_keywords_to_db(name, institution, keywords):
    db = mysql.connector.connect(user='root', password='yEBpALG6zHDoCFLn',
                                 host='104.198.163.126',
                                 database='project')
    cursor = db.cursor()

    for keyword in keywords:
        query = "SELECT occurrence FROM Keywords " \
                "WHERE keyword = %s AND name = %s AND institution = %s"
        val = (keyword, name, institution)
        cursor.execute(query, val)
        data = cursor.fetchall()

        if data:
            occurrence = data[0][0] + 1
            query = "UPDATE Keywords set occurrence = %s " \
                    "WHERE name = %s AND institution = %s AND keyword = %s"
            val = (occurrence, name, institution, keyword)
        else:
            query = "INSERT INTO Keywords (name, institution, keyword, occurrence)" \
                    "VALUES (%s, %s, %s, %s)"
            val = (name, institution, keyword, 1)

        cursor.execute(query, val)

    db.commit()
    db.close()


def del_local_download():
    if os.path.exists(local_filename):
        os.remove(local_filename)


def get_pdf_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find('div', class_='gsc_vcd_title_ggi')
    if container is None:
        return None
    return container.find('a', href=True)['href']


def main():
    """
    input: (professor name: string, professor institution: string, paper url: string) (week 1 just have fixed urls)
    extract keywords for this paper
    and send output keywords to database (for future implementation)
    :return: void
    """

    test_prof_name = 'Kevin Chang'
    # test_prof_name = 'Jiawei Han'
    test_institution = 'University of Illinois at Urbana Champaign'

    # for url in test_pdf_urls:
    #     download_pdf_from_url(url)
    #     keywords = extract_keywords_from_pdf()
    #     update_keywords_to_db(test_prof_name, test_institution, keywords)

    for suffix in test_google_scholar_urls:
        url = google_scholar_prefix + suffix
        pdf_link = get_pdf_link(url)
        if pdf_link is None:
            description = scrape_description(url)
            keywords = extract_keywords_from_description(description)
            update_keywords_to_db(test_prof_name, test_institution, keywords)
        else:
            download_pdf_from_url(pdf_link)
            keywords = extract_keywords_from_pdf()
            update_keywords_to_db(test_prof_name, test_institution, keywords)
            del_local_download()

