import operator
import nltk
from textblob import TextBlob
from textblob import Word
import re
#import ve
from collections import defaultdict


def extractWordPosPredicate(word, line,after):
	numofwords = len(word.split())
	i=0
	#print "WordPOSPREDICATE",word,line
	w = Word(word.split()[0])
	result = list()
	found = 0
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
					found = 1
					if after==1:
						result.append(i+numofwords)						#Returns the position from where we have to take n gram after
					else:
						result.append(i - 1)   							#Returns the position from where we have to take n gram before
		
		i+=1

	if found == 1:
		return result
	else:
		return [-1]

def extractWordPos(word, line,after):
	numofwords = len(word.split())
	i=0
	flag = 0
	result = list()
	
	while i <= (len(line.split()) - numofwords):
		matchflag = 0
		for word1 in zip(word.split(),line.split()[i:i+numofwords]):
			try:
				if Word(word1[0].encode('utf-8')).lemmatize("v") != Word(word1[1].encode('utf-8')).lemmatize("v"):
					matchflag = 1
					break
			except:
				if word1[0]!=word1[1]:
					matchflag = 1
					break
			#if after == 0:
				#print "seed_word", seed_word
				#print "line ",line
			if matchflag == 0:
				if after==1:
					flag = 1
					result.append(i+numofwords)						#Returns the position from where we have to take n gram after
				else:
					flag = 1
					result.append(i - 1)   							#Returns the position from where we have to take n gram before
		i+=1
	if flag == 0:
		return [-1]
	else:
		return result


def predict(tweet):
	positivewords = open("positivewords.txt","r")
	negativewords = open("negativewords.txt","r")
	positivepredicatewords = open("positivepredicatewords.txt","r")
	for word in positivewords:
		poslist = extractWordPos(word, tweet.strip(), 1)
		for pos in poslist:
			if pos!=-1:
			#print word
				for word1 in negativewords:
					pos1list = extractWordPos(word1, tweet.strip(), 0)
					for pos1 in pos1list:
						if pos1!=-1:
							if abs(pos - pos1)<6:								#Can change as required
							#print word1
								return "SARCASM"
	for word in positivepredicatewords:
		poslist = extractWordPosPredicate(word, tweet.strip(), 1)
		for pos in poslist:
			if pos!=-1:
				#print  word
				for word1 in negativewords:
					pos1list = extractWordPos(word1, tweet.strip(), 0)
					pos1afterlist = extractWordPos(word1, tweet.strip(), 1)
					for pos1 in pos1list:
						if pos1!=-1:
							if abs(pos - pos1)<6: 
								return "SARCASM"
					for pos1after in pos1afterlist:
						if pos1after!=-1:
							if abs(pos - pos1after) < 6:
								return "SARCASM"
	return "NOT_SARCASM"

file1 = open("resultsFile.txt","w")
file1.write("")
file1.close()
positivewords = open("positivewords.txt","r")
negativewords = open("negativewords.txt","r")
positivepredicatewords = open("positivepredicatewords.txt","r")

testFile = open("test.tweet","r")
for line in testFile:
	with open("resultsFile.txt","a") as myFile:
		#print line
		myFile.write(predict(line)+"\n")