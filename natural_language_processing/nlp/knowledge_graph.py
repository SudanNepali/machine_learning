import requests
import re
from bs4 import BeautifulSoup
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
from spacy.tokens import Span
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from tqdm import tqdm
"""scrapping text from the given webpage"""
link='https://english.onlinekhabar.com/going-to-annapurna-region-first-go-to-dhampus-instead.html'
link1='https://en.wikipedia.org/wiki/Nepal'
def scrapping(link):
    html=requests.get(link).content
    unicode_str = html.decode("utf8")
    encoded_str = unicode_str.encode("ascii", 'ignore')
    news_soup = BeautifulSoup(encoded_str, "html.parser")
    a_text = news_soup.find_all('p')
    scrapped_text = [re.sub(r'<.+?>', r'', str(a)) for a in a_text]
    return scrapped_text
'''preprocessing the text and extracting entity pairs'''

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

"""Extracting relations"""

def get_relation(sent):

  doc = nlp(sent)


  matcher = Matcher(nlp.vocab)


  pattern = [{'DEP':'ROOT'},
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},
            {'POS':'ADJ','OP':"?"}]

  matcher.add("matching_1", None, pattern)

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]]

  return(span.text)


entity_pairs = []
from tqdm import tqdm
for i in tqdm(scrapping(link1)):
  entity_pairs.append(get_entities(i))
relations = [get_relation(i) for i in tqdm(scrapping(link1))]

"""plotting the graph"""
source = [i[0] for i in entity_pairs]
target = [i[1] for i in entity_pairs]
kg_df = pd.DataFrame({'source': source, 'target': target, 'edge': relations})
db = nx.from_pandas_edgelist(kg_df, "source", "target", 'edge', create_using=nx.MultiDiGraph())
plt.figure(figsize=(15,15))
pos = nx.spring_layout(db)
nx.draw(db, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()
