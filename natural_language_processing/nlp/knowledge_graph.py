import nltk
from nltk import sent_tokenize, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
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
link0='https://english.onlinekhabar.com/going-to-annapurna-region-first-go-to-dhampus-instead.html'
link1='https://en.wikipedia.org/wiki/Nepal'
link3='https://en.wikipedia.org/wiki/Kathmandu_Valley'
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
        stop_words = set(stopwords.words('english'))
        if tok not in stop_words:
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


"""plotting the graph"""
def plot_graph(link):
    entity_pairs = []
    from tqdm import tqdm
    for i in tqdm(scrapping(link)):
      entity_pairs.append(get_entities(i))
    relations = [get_relation(i) for i in tqdm(scrapping(link))]
    porter = PorterStemmer()
    lemma=WordNetLemmatizer()
    source1 = [i[0] for i in entity_pairs]
    source2=[lemma.lemmatize(word) for word in source1]
    source=[porter.stem(word) for word in source1]
    target1 = [i[1] for i in entity_pairs]
    target2=[lemma.lemmatize(word) for word in target1]
    target=[porter.stem(word) for word in target1]

    kg_df = pd.DataFrame({'source': source2, 'target': target2, 'edge': relations})
    db = nx.from_pandas_edgelist(kg_df, "source",'target', edge_attr=True, create_using=nx.MultiDiGraph())
    plt.figure(figsize=(15,15))
    pos = nx.spring_layout(db)
    nx.draw(db, with_labels=True, node_color='skyblue',node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
    plt.show()
    print(source)
    while(True):
        cond=input("do you wish to continue: y/n")
        query = input("Enter your query:")
        if query in source:
            print(target[source.index(query)])
        if cond=='n':
            break

plot_graph(link1)





