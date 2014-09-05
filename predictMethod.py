import operator
import nltk
from textblob import TextBlob
from textblob import Word
import re
#import ve
from collections import defaultdict


def extractWordPos(word, line,after):
	numofwords = len(word.split())
	i=0
	while i <= (len(line.split()) - numofwords):
		if word.split() == line.split()[i:i+numofwords]:
			if after==1:
				return i+numofwords						#Returns the position from where we have to take n gram after
			else:
				return i - 1   							#Returns the position from where we have to take n gram before
		else:
			i+=1
	return -1


def extractWordPosPredicate(word, line,after):
	numofwords = len(word.split())
	i=0
	w = Word(word.split()[0])
	while i <= (len(line.split()) - numofwords):
		if re.match("[A-Za-z]+$",line.split()[i]):
			w = Word(word.split()[0])
			w1 = Word(line.split()[i])
			if w.lemmatize("v") == w1.lemmatize("v"):
				j = 1
				flag = 0
				for j in xrange(numofwords):
					#print line.split()[i+j],word.split()[j],numofwords
					if re.match("^[A-Za-z]+$",line.split()[i+j]):
						w = Word(word.split()[j])
						w1 = Word(line.split()[i+j])
						if w.lemmatize("v") != w1.lemmatize("v"):
							flag = 1
							break
				if flag == 0:
					if after==1:
						return i+numofwords						#Returns the position from where we have to take n gram after
					else:
						return i - 1   							#Returns the position from where we have to take n gram before
		
		i+=1

	return -1

def predict(tweet):
	positivewords = open("positivewords.txt","r")
	negativewords = open("negativewords.txt","r")
	positivepredicatewords = open("positivepredicatewords.txt","r")
	for word in positivewords:
		pos = extractWordPos(word, tweet.strip(), 1)
		if pos!=-1:
			for word1 in negativewords:
				pos1 = extractWordPos(word1, tweet.strip(), 0)
				if pos1!=-1:
					if abs(pos - pos1)<6:								#Can change as required
						return 1
	for word in positivepredicatewords:
		pos = extractWordPosPredicate(word, tweet.strip(), 1)
		if pos!=-1:
			for word1 in negativewords:
				pos1 = extractWordPos(word1, tweet.strip(), 0)
				pos1after = extractWordPos(word1, tweet.strip(), 1)
				if pos1!=-1:
					if abs(pos - pos1)<6 or abs(pos - pos1after) < 6:
						return 1
	return -1

def mainPredict(testFileName):
	positivewords = open("positivewords.txt","r")
	negativewords = open("negativewords.txt","r")
	positivepredicatewords = open("positivepredicatewords.txt","r")

	testFile = open(testFileName,"r")
	results = list()
	for line in testFile:
		results.append(predict(line))

	return results