"""
Knowledge Base Reference: https://www.kaggle.com/Cornell-University/arxiv
"""

import pandas as pd
import json
from collections import Counter, defaultdict
from tqdm.notebook import tqdm

def get_metadata():
    # Make Relative Paths (https://stackoverflow.com/questions/918154/relative-paths-in-python)
    with open('/Users/bhave/Desktop/Forward_Data_Lab_Education_Today/backend/data/arxiv-metadata-oai-snapshot.json') as f:
        for line in f:
            yield line


metadata = get_metadata()

for paper in metadata:
    first_paper = json.loads(paper)
    break


for key in first_paper:
    print(key)


for key in first_paper:
    if key != 'abstract':
        print(first_paper[key])

print(first_paper['authors'])
print(first_paper['authors_parsed'])
print(first_paper['doi'])


# DataFrame
column_names = ["ids", "jref","doi", "title","submitter"]
dfOut = pd.DataFrame(columns = column_names)


ids = []
jref = []
doi = []
title = []
submit = []

metadata = get_metadata()
n_journal_publicated = 0

for ind, paper in enumerate(metadata):
    paper = json.loads(paper)
    if paper['journal-ref'] != None:
        #tempDict = {}
        n_journal_publicated += 1
        #tempDict['ids'] = paper['id']
        #tempDict['jref'] = paper['journal-ref']
        #tempDict['doi'] = paper['doi']
        #tempDict['title'] = paper['title']
        #tempDict['submitter'] = paper['submitter']
        
        ids.append(paper['id'])
        jref.append(paper['journal-ref'])
        doi.append(paper['doi'])
        title.append(paper['title'])
        submit.append(paper['submitter'])
        
        
        #dfOut = dfOut.append(tempDict, ignore_index=True)

print(f'Number of papers publicated in journals is: {n_journal_publicated}')