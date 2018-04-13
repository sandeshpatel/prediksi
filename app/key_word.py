#!/usr/bin/env python
df = {}
with open('doc_freq_36lac.txt') as file:
    for line in file:
        tokens = line.split()
        df[tokens[0]] = int(tokens[1])
print(len(df))
        

import numpy as np
idf = {}
for word in df:
    idf[word] = np.log(3620000 /(1+ df[word])) #3620000 is the number of document processed




tf = {}
with open('sample.txt') as sample:
    for line in sample:
        for word in line.split():
            word = word.lower()
            if word in df:
                if word in tf:
                    tf[word] += 1
                else:
                    tf[word] = 1



tfidf = {}
for word in tf:
    tfidf[word] = tf[word] * idf[word]


# In[77]:


import operator
keywords = ""
tfidf_sorted = sorted(tfidf.items(), key=operator.itemgetter(1))[::-1]
for i in range(7):
    keywords += tfidf_sorted[i][0] + ' '



import sys

class Node:
	def __init__(self):

		node = {}
		node['next'] = {}	#Initialize an empty hash (python dictionary)

		node['word_marker'] = False 
		# There can be words, Hot and Hottest. When search is performed, usually state transition upto leaf node is peformed and characters are printed. 

		# Then in this case, only Hottest will be printed. Hot is intermediate state. Inorder to mark t as a state where word is to be print, a word_marker is used
		return node



	def add_item(self, string):
		''' Method to add a string the Trie data structure'''
		
		if len(string) == 0:
			self.word_marker = True 
			return 
		
		key = string[0] #Extract first character

		string = string[1:] #Create a string by removing first character


		# If the key character exists in the hash, call next pointing node's add_item() with remaining string as argument

		if key in self.next:
			self.next[key].add_item(string)
		# Else create an empty node. Insert the key character to hash and point it to newly created node. Call add_item() in new node with remaining string.

		else:
			node = Node()
			self.next[key] = node
			node.add_item(string)


	def dfs(self, sofar=None):
		'''Perform Depth First Search Traversal'''
		
		# When hash of the current node is empty, that means it is a leaf node. 

		# Hence print sofar (sofar is a string containing the path as character sequences through which state transition occured)

		if self.next.keys() == []:
			print("Match:",sofar)
			return
			
		if self.word_marker == True:
			print("Match:",sofar)

		# Recursively call dfs for all the nodes pointed by keys in the hash

		for key in self.next.keys():
			self.next[key].dfs(sofar+key)

	def search(self, string, sofar=""):
		'''Perform auto completion search and print the autocomplete results'''
		# Make state transition based on the input characters. 

		# When the input characters becomes exhaused, perform dfs() so that the trie gets traversed upto leaves and print the state characters

		if len(string) > 0:
			key = string[0]
			string = string[1:]
			#if key in self.next:
			if key in self.next:
				sofar = sofar + key
				self.next[key].search(string,sofar)
				
			else:
				print("No match")
		else:
			if self.word_marker == True:
				print("Match:",sofar)

			for key in self.next.keys():
				self.next[key].dfs(sofar+key)


def fileparse():
	from googlesearch import search
	import requests
	from bs4 import BeautifulSoup
	import re
	regex = re.compile(r"\W")
	root = Node()
	text = []
	print(keywords)
	for url in search(keywords, stop=20):
		try:
			r = requests.get(url)
			soup = BeautifulSoup(r.text, 'html.parser')
			for sent_array in [s.findAll(text=True) for s in soup.findAll('p')]:
				#sent_array is a list of sentances of a paragraph
				for sentance in [regex.sub(" ", sent).split() for sent in sent_array]:
					text.extend(sentance)
					#print(sentance)
					try:
						text.extend([sentance[i] + ' ' + sentance[i+1] for i in range(len(sentance)-1)])
					except:
						pass
		except:
			pass
	for word in text:
		if 1<len(word)< 50:
			root.add_item(word.lower())
			#print(word)
	return root



if __name__ == '__main__':
	root  = fileparse()
	again = '1'
	while again != '0':
		again = input('enter query or 0 to exit ')
		if again != '0':
			root.search(again)
