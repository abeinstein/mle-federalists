# Federalist Papers!
import string
import document
import collections
import math
import matplotlib.pyplot as plt

HAMILTON_PAPERS = ["federalist/hamilton" + str(i) +".txt" for i in xrange(1,16)]
MADISON_PAPERS = ["federalist/madison" + str(i) +".txt" for i in xrange(1, 16)]
UNKNOWN_PAPERS = ["federalist/unknown" + str(i) + ".txt" for i in xrange(1, 12)]

def cross_validate(hamilton_docs, madison_docs, gamma):
	''' Calculates the error rate using cross-validation in order to find the 
	best gamma value.
	'''
	num_correct = 0
	num_incorrect = 0
	margin = 0
	for i in range(30):
		if i < 15:
			training_docs_hamilton = hamilton_docs[:i] + hamilton_docs[i+1:]
			training_docs_madison = madison_docs
			test_doc = hamilton_docs[i]
		else:
			training_docs_hamilton = hamilton_docs
			j = i - 15
			training_docs_madison = madison_docs[:j] + madison_docs[j+1:]
			test_doc = madison_docs[j]
		hamilton_word_counts = get_combined_wcs(training_docs_hamilton)
		madison_word_counts = get_combined_wcs(training_docs_madison)
		hamilton_thetas = get_thetas(hamilton_word_counts, gamma)
		madison_thetas = get_thetas(madison_word_counts, gamma)
		hamilton_LL = get_log_likelihood(test_doc, hamilton_thetas)
		madison_LL = get_log_likelihood(test_doc, madison_thetas)

		if hamilton_LL > madison_LL:
			author = "Hamilton"
		else:
			author = "Madison"

		print test_doc.file_path, " & ", hamilton_LL, " & ", madison_LL, " & ", author, " \\\\ "

		if i < 15:
			margin += hamilton_LL - madison_LL
			if author == "Hamilton":
				num_correct += 1
			else:
				num_incorrect += 1	
		else:
			margin += madison_LL - hamilton_LL
			if author == "Madison":
				num_correct += 1	
			else:
				num_incorrect += 1
				
	error = float(num_incorrect)/(num_correct + num_incorrect)
	print margin / 30 # Prints the average distance 
	return error



def get_combined_wcs(list_of_docs):
	''' Gets the combined word frequency list from a list of Documents.'''
	combined_wcs = collections.defaultdict(int)
	for doc in list_of_docs:
		for word, count in doc.word_counts.iteritems():
			combined_wcs[word] += count
	return combined_wcs

def get_thetas(word_counts, gamma):
	'''Returns a dictionary containing theta values'''
	thetas = collections.defaultdict(lambda: gamma)
	total_words = len(word_counts.keys())
	total_count = sum(word_counts.values())
	denom = float(total_count) + total_words*gamma
	for word, count in word_counts.iteritems():
		thetas[word] = (count + gamma) / denom
	return thetas

def get_log_likelihood(test_doc, thetas):
	''' Returns the log likelihood'''
	const = get_const(test_doc)
	log_like = const
	for word, count in test_doc.word_counts.iteritems():
		log_like += count*math.log(thetas[word])
	return log_like

def get_const(test_doc):
	''' Returns the constant used in the log-likelihood'''
	n = sum(test_doc.word_counts.values())
	k = len(test_doc.word_counts)
	first_term = 0
	for i in xrange(1, n+1):
		first_term += math.log(i)

	second_term = 0
	for count in test_doc.word_counts.values():
		second_term += math.log(math.factorial(count))

	return first_term - second_term

def find_optimal_gamma(hamilton_docs, madison_docs):
	'''Method used to find the optimal gamma'''
	GAMMA_VALS = [.0000001, .000001, .00001, .0001, .001, .01, 1, 10, 100]
	errors = {}
	for gamma in GAMMA_VALS:
		err = cross_validate(hamilton_docs, madison_docs, gamma)
		errors[gamma] = err
	return errors

def plot_gammas(errors):
	'''Plots the gamma values using matplotlib.pyplot'''
	plt.plot(map(math.log, errors.keys()), errors.values(), 'c*')
	plt.xlabel("Log of Gamma Value")
	plt.ylabel("Cross-validation Error Rate")
	plt.ylim([0,1])
	plt.show()

def train(docs):
	'''Trains documents using the optimal gamma value (.0001)'''
	word_counts = get_combined_wcs(docs)
	thetas = get_thetas(word_counts, .0001)
	return thetas

def classify(test_doc, hamilton_docs, madison_docs):
	'''Predicts the author of test_doc'''
	hamilton_thetas = train(hamilton_docs)
	madison_thetas = train(madison_docs)
	hamilton_prob = get_log_likelihood(test_doc, hamilton_thetas)
	madison_prob = get_log_likelihood(test_doc, madison_thetas)

	#print hamilton_prob, madison_prob
	if hamilton_prob > madison_prob:
		test_doc.author = "Hamilton"
		#return "Hamilton"
	else:
		test_doc.author = "Madison"
		#return "Madison"

	print test_doc.file_path, " & ", hamilton_prob, " & ", madison_prob, " & ", test_doc.author + " \\\\ "

if __name__ == "__main__":
	hamilton_docs = []
	madison_docs = []
	unknown_docs = []
	for hamilton_file in HAMILTON_PAPERS:
		d = document.Document(hamilton_file, "Hamilton")
		hamilton_docs.append(d)
	for madison_file in MADISON_PAPERS:
		d = document.Document(madison_file, "Madison")
		madison_docs.append(d)
	for unknown_file in UNKNOWN_PAPERS:
		d = document.Document(unknown_file, "Unknown")
		unknown_docs.append(d)

	# UNCOMMENT TO PLOT GAMMA VALUES
	# errors = find_optimal_gamma(hamilton_docs, madison_docs)
	# plot_gammas(errors)

	# UNCOMMENT TO GET CROSS-VALIDATION RESULTS
	# err = cross_validate(hamilton_docs, madison_docs, .0001)
	# print "Error: ", err
	
	# UNCOMMENT TO PREDICT AUTHORSHIP OF UNKNOWN DOCUMENTS
	# for doc in unknown_docs:
	#  	classify(doc, hamilton_docs, madison_docs)



	
	

	
	




