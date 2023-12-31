import re
import os
import sys

import pandas as pd
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
from bs4 import BeautifulSoup
import unicodedata
from textblob import TextBlob

nlp = spacy.load('C:/Users/Deepak Ramamurthy/Downloads/en_core_web_sm-3.7.1/en_core_web_sm/en_core_web_sm-3.7.1')

def _get_wordcounts(x):
	length = len(str(x).split())
	return length

def _get_charcounts(x):
	s = x.split()
	x = ''.join(s)
	return len(x)

def _get_avg_wordlength(x):
	count = _get_charcounts(x) / _get_wordcounts(x)
	return count

def _get_stopwords_count(x):
	l = len([t for t in str(x).split() if t in stopwords])
	return l

def _get_hashtag_counts(x):
	l = len([t for t in str(x).split() if t.startswith('#')])
	return l

def _get_mentions_counts(x):
	l = len([t for t in str(x).split() if t.startswith('@')])
	return l

def _get_digit_count(x):
	return len([t for t in str(x).split() if t.isdigit()])

def _get_uppercase_counts(x):
	return len([t for t in str(x).split() if t.isupper()])

def _get_lowercase(x):
	return str(x).lower()

def _get_emails(x):
	emails = re.findall(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)', x)
	counts = len(emails)

	return counts, emails

def _remove_emails(x):
	return re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"",x)

def _get_urls(x):
	urls = re.findall(r'(https|http|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', x)
	counts = len(urls)

	return counts, urls

def _remove_urls(x):
	return re.sub(r'(https|http|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', "",x)

def _remove_rt(x):
	return re.sub(r'\brt\b', '', x).strip()

def _remove_spchr_punct(x):
	x = re.sub(r'[^\w ]+','',x)
	x = ' '.join(x.split())
	return x

def _remove_html_tags(x):
	return BeautifulSoup(x, 'lxml').get_text().strip()

def _remove_accented_chars(x):
	x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore')
	return x

def _remove_stopwords(x):
	return ' '.join([t for t in x.split() if t not in stopwords])

def _make_base(x):
	x = str(x)
	x_list = []
	doc = nlp(x)
	
	for token in doc:
		lemma = token.lemma_
		if lemma == '-PRON-' or lemma == 'be':
			lemma = token.text
		x_list.append(lemma)
	return ' '.join(x_list)

def _get_value_counts(df, col):
	text = ' '.join(df['col'])
	text = text.split()
	freq = pd.Series(text).value_counts()
	return freq



def _remove_common_words(x, freq, n=20):
	fn = freq[:n]
	x = ' '.join([t for t in x.split() if t not in fn])
	return x

def _remove_rare_words(x, freq, n=20):
	fn = freq.tail[:n]
	x = ' '.join([t for t in x.split() if t not in fn])
	return x

def _spelling_correction(x):
	x = TextBlob(x).correct()
	return x
