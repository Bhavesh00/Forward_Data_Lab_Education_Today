import PyPDF2
import textract
import nltk
# nltk.download()
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def test_extract():
    filename = 'Insights from Student Solutions to SQL Homework Problems.pdf'
    # filename = 'MetaGCN-ASONAM2019-AravindSankar-201907.pdf'
    # filename = 'test file.pdf'
    #
    # pdf_file = open(filename, 'rb')
    # file = PyPDF2.PdfFileReader(pdf_file)
    # num_pages = file.numPages
    #
    # text = ""
    # for i in range(num_pages):
    #     page = file.getPage(i)
    #     text += page.extractText()
    #     # print(page.extractText())

    text = textract.process(filename, method='pdfminer')


    print(text)
    # tokens = nltk.word_tokenize(text)
    # print(tokens)
    # pdf_file.close()


if __name__ == '__main__':
    test_extract()

