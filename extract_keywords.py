import string
import requests
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import nltk
# nltk.download()
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# [1] has built-in keywords
normal_pdf_urls = ["https://www.researchgate.net/profile/Abdussalam_Alawini/publication"
                   "/325090722_Provenance_Analysis_for_Missing_Answers_and_Integrity_Repairs/links"
                   "/5af5aaec0f7e9b026bceafec/Provenance-Analysis-for-Missing-Answers-and-Integrity-Repairs.pdf",
                   "https://educationaldatamining.org/files/conferences/EDM2020/papers/paper_150.pdf",
                   "http://sites.computer.org/debull/A18mar/p27.pdf",
                   "http://sites.computer.org/debull/A18mar/p39.pdf"]

# [3] has built-in keywords
google_drive_pdf_urls = ["https://drive.google.com/file/d/1iYsVVlMo57OENah9tc0oNJaBV02jcMqc",
                         "https://drive.google.com/file/d/1i2FWf2DwYtOsTTj79dm9ujnago4PB9Io",
                         "https://drive.google.com/file/d/1DGLaDupsKVvL04-8mdOHKxycyy114Hnj",
                         "https://drive.google.com/file/d/1xH8Ekrs5-3waR_udmoNoZ3bHvrm8GEzr"]

local_filename = "download.pdf"


def extract_keywords_from_pdf():
    pdf_string = convert_pdf_to_str()
    # print(pdf_string)
    already_have_keywords_or_index_term()

    # tokens = nltk.word_tokenize(pdf_string)
    # tokens = list(filter(lambda token: token.lower() not in string.punctuation, tokens))
    # tokens = list(filter(lambda token: token.lower() not in stopwords.words('english'), tokens))
    # print(tokens)


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


def already_have_keywords_or_index_term():
    pass


def download_pdf_from_url(url: str):
    if "drive.google" in url:
        download_pdf_from_google_drive_url(url)
        return
    download_pdf_from_normal_url(url)


def download_pdf_from_normal_url(url: str):
    r = requests.get(url, stream=True)

    with open(local_filename, 'wb') as f:
        f.write(r.content)


def download_pdf_from_google_drive_url(url: str):
    print("get google drive url")


def main():
    """
    input: (professor name: string, professor institution: string, paper url: string) (week 1 just have fixed urls)
    extract keywords for this paper
    and send output keywords to database (for future implementation)
    :return: void
    """

    url = normal_pdf_urls[0]
    # url = google_drive_pdf_urls[0]
    # url = "http://www.africau.edu/images/default/sample.pdf"

    download_pdf_from_url(url)
    extract_keywords_from_pdf()

