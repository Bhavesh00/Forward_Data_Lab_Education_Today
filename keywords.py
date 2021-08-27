import os
import json
#print(os.path.abspath("arxiv-metadata-oai-snapshot.json"))
print("*****************************START***************************\n*************************************************************")
in_file_path = 'filtered_arxiv.json'

titleAbstractDict = {}
with open(in_file_path,'r') as in_json_file:
    json_obj_list = json.load(in_json_file)
    count = 0
    for json_obj in json_obj_list:
        if count > 1000:
            break
        titleAbstractDict[json_obj["title"]] = json_obj["abstract"]
        count += 1

'''********************
getSentences function
PARAMETERS:  KEYWORD -- word to search for; TEXT -- string made of sentence(s)
RETURN: a list of strings, each is a sentence containing the keyword
************************'''
def getSentences(keyword, text):
    sentences = []
    startIdx = 0
    for charIdx in range(len(text)):
        if text[charIdx]=='.':
            if keyword.lower() in text[startIdx:charIdx].lower():
                if startIdx == 0:
                    sentences.append(text[startIdx:charIdx+1])
                sentences.append(text[startIdx+2:charIdx+1])
            startIdx = charIdx
    return sentences
 
trialKey = "dynamic programming"
trialOutputList = []
for title in titleAbstractDict:
    if trialKey in titleAbstractDict[title]:
        sentenceList = getSentences(trialKey, titleAbstractDict[title])
        for sentence in sentenceList:
            trialOutputList.append(sentence)
    if len(trialOutputList)>5:
        break

print(trialOutputList)
'''trialTxt = "CS. uiuc cs department is one of the best CS department in the US. One of the best courses offered in UIUC is database system. Database System offers information about sql and data structures."
print("1:",getSentences("cs", trialTxt))
print("2:",getSentences("uiuc", trialTxt))
print("3:",getSentences("UIUC", trialTxt))
print("4:",getSentences("database System", trialTxt))'''
