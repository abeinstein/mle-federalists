import nltk
import collections
import string
import document

def stem_dict(paper_file):
	''' Uses the Snowball Stemmer and the NLTK module to stem words'''
	word_counts = collections.defaultdict(int)
	for line in paper_file:
		line = line.translate(string.maketrans("",""), string.punctuation)
		words = line.split()
		snowball_stemmer = nltk.stem.snowball.EnglishStemmer()
		words = map(snowball_stemmer.stem, words)
		for w in words:
			word_counts[w] += 1
	return word_counts

def most_frequent_words_dict(paper_file, num_words=20):
	''' Uses only the most frequent words '''
	word_counts = document.get_counts3(paper_file)
	top_words = sorted(word_counts.keys(), key=word_counts.get, reverse=True)[:num_words]
	most_frequent_words = {}
	for w in word_counts:
		if w in top_words:
			most_frequent_words[w] = word_counts[w]
	return most_frequent_words

def remove_most_frequent_words(paper_file, num_words=20):
	''' Removes the most frequent words '''
	word_counts = document.get_counts3(paper_file)
	top_words = sorted(word_counts.keys(), key=word_counts.get, reverse=True)[:num_words]
	no_most_frequent_words = {}
	for w in word_counts:
		if w not in top_words:
			no_most_frequent_words[w] = word_counts[w]
	return no_most_frequent_words






