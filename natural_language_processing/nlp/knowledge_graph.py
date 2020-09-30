from bs4 import BeautifulSoup
import requests
import re
import string
"""Scrapping Text from onlinekhabar"""
html=requests.get('https://english.onlinekhabar.com/things-not-to-do-while-trekking-in-nepali-himalayas.html').content
unicode_str = html.decode("utf8")
encoded_str = unicode_str.encode("ascii",'ignore')
news_soup = BeautifulSoup(encoded_str, "html.parser")
a_text = news_soup.find_all('p')
scrapped_text=[re.sub(r'<.+?>',r'',str(a)) for a in a_text]
scrapped=str(scrapped_text)
#print(scrapped_text)
"""Cleaning the text for further operations using"""
import spacy
from spacy import displacy
nlp=spacy.load("en_core_web_sm")
#doc=nlp(scrapped)
#for sent in doc.sents:
    #for tok in sent:
        #print(tok.text,'...',tok.dep_)

'''Extracting subject objects entities modifiers'''
def get_entities(sent):
    ent1 = ""
    ent2 = ""

    prv_tok_dep = ""
    prv_tok_text = ""

    prefix = ""
    modifier = ""



    for tok in nlp(sent):
        if tok.dep_ != "punct":
            if tok.dep_ == "compound":
                prefix = tok.text
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " " + tok.text
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " " + tok.text

            if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""

            if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text
            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text
    return [ent1.strip(), ent2.strip()]

entity_pairs = []
from tqdm import tqdm
for i in tqdm(scrapped_text):
  entity_pairs.append(get_entities(i))

#print(entity_pairs[10:20])

'''building graph'''
