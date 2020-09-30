import nltk
from nltk.corpus import movie_reviews
#print(movie_reviews.fileids())
movie_reviews_raw=movie_reviews.raw('neg/cv000_29416.txt')
#print(movie_reviews_raw)
"""tokenizing and removing punctuations and nonalphabetic tokens"""
from nltk import word_tokenize
#movie_reviews_sents=movie_reviews.sents("neg/cv000_29416.txt")
movie_reviews_token=word_tokenize(movie_reviews_raw)
movie_reviews_words = [word for word in movie_reviews_token if word.isalpha()]
"""convert to lowercase"""
movie_reviews_lower=[word.lower()for word in movie_reviews_words]
#print(words[:100])
"""Filter out stop words"""
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
movie_reviews_lower = [w for w in movie_reviews_lower if not w in stop_words]
print(movie_reviews_lower[:100])
"""Stemming"""
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()
movie_reviews_stemmed = [porter.stem(word) for word in movie_reviews_lower]
print(movie_reviews_stemmed[:100])
"""lammetization"""
from nltk.stem import WordNetLemmatizer
word_lemmatizer = WordNetLemmatizer()
for w in movie_reviews_lower:
    print(f'Actual Word - {w}')
    print(f'Lemma - {word_lemmatizer.lemmatize(w)}\n')
"""part of speech tagging"""
print(nltk.pos_tag(movie_reviews_lower))


#print(movie_reviews_sents)

