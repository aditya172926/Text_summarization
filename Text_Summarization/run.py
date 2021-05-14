import nltk
import os
import re
import spacy
import sys
import unicodedata

import networkx as nx
import numpy as np
import pandas as pd 
 
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity

# Root directory
root = '.'
# Loading Spacy for Parts-of-Speech tagging.
nlp_spacy = spacy.load('en_core_web_sm')
# Loading list of stopwords
stop_words = stopwords.words('english')




"""
	For TextRank Algorithm.
"""
def remove_extraneous_text(sentence:str)->str:
	"""
		Input: String
		Output: String
		Takes a news article as input and removes extra spaces and reporting location from it.
	"""
	# Remove multiple spaces
	sentence = re.sub(" +", " ", sentence)

	# Remove reporting location
	if ") --" in sentence:
		sentence = sentence.split(") --")[-1]

	# Remove media name from article
	if "(CNN)" in sentence:
		sentence = sentence.split("(CNN)")[-1]

	return sentence

def remove_stopwords(sentence:str)->str:
	"""
		Input: String
		Output: String
		Takes a sentence as input and returns the sentence after removing all stopwords.
	"""
	sentence = " ".join([word for word in sentence.split() if word not in stop_words])

	return sentence

def lemmatize_text(sentence:str)->str:
	"""
		Input: String
		Output: String
		Takes a sentence as input and uses Spacy to convert each word into it's lemma.
	"""
	sentence = nlp_spacy(sentence)
	sentence = ' '.join([word.lemma_ if word.lemma_ != "-PRON-" else word.text for word in sentence])
	return sentence

def clean_text(sentence:str)->str:
	"""
		Input: String
		Output: String
		Takes a sentence and cleans by:
		 - Converting to lowercase
		 - Remove non alphabetic characters
		 - Removing extraneous characters
		 - Removing stopwords
		 - Lemmatizing words
	"""
	sentence = sentence.lower()
	sentence = re.sub("[^a-zA-Z]", " ", sentence)
	sentence = remove_extraneous_text(sentence)
	sentence = remove_stopwords(sentence)
	sentence = lemmatize_text(sentence)
	return sentence




"""
	For Feature Term enhancements.
"""
def get_total_terms(cleaned_sentences:list)->int:
	"""
		Input: List
		Output: Int
		Takes in a list of sentences and returns total number of tokens in those sentences.
	"""
	total_terms = 0

	for sentence in cleaned_sentences:
		total_terms += len(sentence.split())

	return total_terms

def get_term_frequencies(cleaned_sentences:list)->dict:
	"""
		Input: List
		Output: Dict
		Takes in a list of sentences and returns a dictionary containing Tokens as keys and their frequencies as values.
	"""
	freq_dict = {}

	for sentence in cleaned_sentences:
		for word in sentence.split():
			freq_dict[word] = freq_dict.get(word, 0) + 1

	return freq_dict

def get_term_weights(cleaned_sentences:list)->dict:
	"""
		Input: List
		Output: Dict
		Takes in a list of sentences and returns a dictionary containing Tokens as keys and their weightage as values.
		The weight is calculated using formula:
					TW(ti) = (TF(ti) * 1000) / (Nt)
		where ti is each token, TW is term weight, TF is term frequency and Nt is total number of terms
	"""
	total_terms = get_total_terms(cleaned_sentences)
	term_freq_dict = get_term_frequencies(cleaned_sentences)
	term_weights = dict()

	for key, value in term_freq_dict.items():
		term_weights[key] = (value * 1000) / total_terms

	return term_weights

def inverse_sentence_frequency(cleaned_sentences:list)->dict:
	"""
		Input: List
		Output: Dict
		Takes in a list of sentences and returns a dictionary containing Tokens as keys and their inverse sentence frequency as values.
		The inverse sentence frequency is calculated as:
					ISF(ti) = log((Ns) / Nti)
		where ti is each token, ISF is inverse sentence frequency, Ns is total number of sentences in paragraph and Nti are the total number of
		sentences in which ti appeared in that paragraph.
	"""
	vocabulary = set()

	for sentence in cleaned_sentences:
		vocabulary = vocabulary.union(set(sentence.split()))

	isf = dict()
	number_of_sentences = len(cleaned_sentences)

	for word in vocabulary:
		number_of_appearances = 0

		for sentence in cleaned_sentences:
			if word in sentence:
				number_of_appearances += 1

		isf[word] = np.log(number_of_sentences / number_of_appearances)

	return isf

def word_weights(cleaned_sentences:str)->dict:
	"""
		Input: List
		Output: Dict
		Takes in a list of sentences and returns a dictionary containing Tokens as keys and their resultant weightage as values.
		The weightage is calculated as:
					RW(ti) = ISF(ti) * TW(ti)
		where ti is each token, RW is resultant weightage, ISF is inverse sentence frequency and TW is term weightage.
	"""

	term_weights = get_term_weights(cleaned_sentences)
	inverse_sentence_freq = inverse_sentence_frequency(cleaned_sentences)

	resultant_weights = dict()

	for word in term_weights.keys():
		resultant_weights[word] = term_weights[word] * inverse_sentence_freq[word]

	return resultant_weights

def pos_tagging(cleaned_sentences:list)->list:
	"""
		Input: List
		Output: List
		Takes in a list of sentences and returns a list of lists, where each Token is represented as a tuple of the form (Token, POS tag).
	"""
	tagged_sentences = []

	for sentence in cleaned_sentences:
		sentence_nlp = nlp_spacy(sentence)

		tagged_sentence = []

		for word in sentence_nlp:
			tagged_sentence.append((word, word.pos_))

		tagged_sentences.append(tagged_sentence)

	return tagged_sentences

def sentence_weights(tagged_sentences:list, total_terms:int)->list:
	"""
		Input: List, Int
		Output: List
		Takes in a list of POS tagged sentences and total number of terms. Returns a list containing the sentence weight of each sentence.
		The sentence weight is calculated as:
					SW(si) = Number of nouns and verbs in sentence / total number of terms in paragraph.
	"""
	sent_weights = []

	for sentence in tagged_sentences:
		relevance_count = 0

		for word, tag in sentence:
			if tag == 'NOUN' or tag == 'VERB':
				relevance_count += 1

		sent_weights.append(relevance_count / total_terms)

	return sent_weights

def sentence_position(cleaned_sentences:list)->list:
	"""
		Input: List
		Output: List
		Takes in a list of sentences and returns weight for each sentence based on it's position.
	"""
	sent_position = []
	number_of_sentences = len(cleaned_sentences)

	weights = [0, 0.25, 0.23, 0.14, 0.08, 0.05, 0.04, 0.06, 0.04, 0.04, 0.15]

	for i in range(1, len(cleaned_sentences)+1):
		sent_position.append(weights[int(np.ceil(10 * (i / number_of_sentences)))])
	return sent_position

def sentence_length(cleaned_sentences:list)->list:
	"""
		Input: List
		Output: List
		Takes in a list of sentences and returns a list containing length of each sentence.
	"""
	sent_len = []

	for sentence in cleaned_sentences:
		sent_len.append(len(sentence.split()))

	return sent_len




"""
	Functions to rank sentences.
"""
def text_rank(sentences:list, word_embeddings:dict)->dict:
	"""
		Input: List, Dict
		Output: Dict
		Takes a list of sentences and Glove word embeddings as input and returns a dictionary containing sentences index as key and rank as value.
		The ranking is done based on the PageRank algorithm
	"""
	# Clean sentences for PageRank algorithm.
	clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
	clean_sentences = [s.lower() for s in clean_sentences]
	clean_sentences = [remove_stopwords(r) for r in clean_sentences]

	# Replace each word with Glove embeddings. The Sentence vector is the average of the sum of embeddings of all words in that
	# sentence.
	sentence_vectors = []
	for i in clean_sentences:
		if len(i) != 0:
			v = sum([word_embeddings.get(w, np.zeros((100, ))) for w in i.split()]) / (len(i.split()) + 0.001)
		else:
			v = np.zeros((100, ))
		sentence_vectors.append(v)

	# Initialize a similarity matrix for pair of sentences
	sim_mat = np.zeros([len(sentences), len(sentences)])

	# Calculate cosine similarity for each pair of sentences
	for i in range(len(sentences)):
		for j in range(len(sentences)):
			if i != j:
				sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, 100), sentence_vectors[j].reshape(1, 100))[0, 0]

	# Create a PageRank graph using similarity matrix
	nx_graph = nx.from_numpy_array(sim_mat)
	scores = nx.pagerank(nx_graph)

	return scores

def feature_rank(sentences:list)->dict:
	"""
		Input: List
		Output: Dict
		Takes a list of sentences as input and returns a dict containig ranking of each sentence.
		The ranking is calculated using word and sentence level features.
	"""
	cleaned_sentences = [clean_text(sentence) for sentence in sentences]

	term_weights = word_weights(cleaned_sentences)
	tagged_sentences = pos_tagging(cleaned_sentences)
	total_terms = get_total_terms(cleaned_sentences)
	sent_weights = sentence_weights(tagged_sentences, total_terms)
	sent_position = sentence_position(cleaned_sentences)
	sent_len = sentence_length(cleaned_sentences)

	sentence_scores = []

	for index, sentence in enumerate(cleaned_sentences):
		score = 0

		for word in sentence.split():
			score += term_weights[word]

		score *= sent_weights[index]
		score += sent_position[index]

		if sent_len[index] != 0:
			score /= sent_len[index]
		else:
			score = 0

		sentence_scores.append(score)

	sentence_scores = sentence_scores / np.sum(sentence_scores)

	final_scores = dict()

	for i in range(len(sentence_scores)):
		final_scores[i] = sentence_scores[i]

	return final_scores




def main()->None:
	"""
		The driver function.
	"""

	# Path to input file
	input_filepath = os.path.join(root, sys.argv[-1])

	if not os.path.exists(input_filepath):
		# Check if input file does not exist.
		print("Could not find input file at location '%s'" % (input_filepath))
		return

	input_text = ""

	with open(input_filepath, 'r') as f:
		input_text = f.read()



	# Location of Glove word embeddings.
	glove_location = os.path.join(root, 'embeddings', 'glove.6B.100d.txt')

	if not os.path.exists(glove_location):
		# Check if word embeddings do not exist.
		print("Could not find Glove Word Embeddings. Kindly download from 'https://drive.google.com/open?id=1cQBYwoLHZzHk4w8zdgcSPFmOP5Xq-x0z' \
			and save in './embeddings' location.")
		return

	print("Loading Glove Word embeddings.")
	
	# Dictionary to store embeddings
	word_embeddings = {}

	# Open file and load embeddings in memory
	f = open(glove_location, encoding='utf-8')
	for line in f:
		values = line.split()
		word = values[0]
		coefs = np.asarray(values[1:], dtype='float32')
		word_embeddings[word] = coefs
	f.close()

	print("Embeddings loaded.")

	print("Creating summary.")

	sentences = sent_tokenize(input_text)
	text_rank_scores = text_rank(sentences, word_embeddings)
	feature_rank_scores = feature_rank(sentences)

	final_scores = dict()
	for i in range(len(text_rank_scores.keys())):
		final_scores[i] = 0.8 * text_rank_scores[i] + 0.2 * feature_rank_scores[i]

	ranked_sentences = sorted(((final_scores[i], s, i) for i, s in enumerate(sentences)), reverse=True)[:3]
	ranked_sentences = sorted(ranked_sentences, key=lambda x: x[2])

	output_text = ""
	for i in range(len(ranked_sentences)):
		output_text += ranked_sentences[i][1] + ' '

	with open('output.txt', 'w') as f:
		f.write(output_text.strip())
	print("Summary stored in 'output.txt'.")


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("The syntax to run this program is: 'python run.py file_name.txt'")
	else:
		main()