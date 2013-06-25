import collections
import string

class Document:
	'''Represents a single document'''
	def __init__(self, file_path, author=None):
		doc_file = open(file_path, 'r')
		self.file_path = file_path
		self.word_counts = get_counts3(doc_file)
		self.author = author


def get_counts1(paper_file):
	'''Full preprocessing (remove punctuation and make everything lowercase)'''
	word_counts = collections.defaultdict(int)
	for line in paper_file:
		line = line.translate(string.maketrans("",""), string.punctuation)
		words = line.split()
		words = map(string.lower, words)
		for w in words:
			word_counts[w] += 1

	return word_counts

def get_counts2(paper_file):
	'''No preprocessing'''
	word_counts = collections.defaultdict(int)
	for line in paper_file:
		words = line.split()
		for w in words:
			word_counts[w] += 1

	return word_counts

def get_counts3(paper_file):
	'''Just remove punctuation'''
	word_counts = collections.defaultdict(int)
	for line in paper_file:
		line = line.translate(string.maketrans("",""), string.punctuation)
		words = line.split()
		for w in words:
			word_counts[w] += 1

	return word_counts

def get_counts4(paper_file):
	'''Just make everything lowercase'''
	word_counts = collections.defaultdict(int)
	for line in paper_file:
		words = line.split()
		words = map(string.lower, words)
		for w in words:
			word_counts[w] += 1

	return word_counts





