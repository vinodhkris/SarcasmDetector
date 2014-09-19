from collections import defaultdict
from nltk.stem.porter import PorterStemmer
import operator
import nltk
from textblob import TextBlob
from textblob import Word
import re
#import verbs

st = PorterStemmer()			#For implementing stemming later on

file1 = open("positivewords","w")
file1.write("")
file1.close()
file1 = open("negativewords","w")
file1.write("")
file1.close()
file1 = open("positivepredicatewords","w")
file1.write("")
file1.close()
#Prepare the files
def seedPOS(inputFile):
	#Requires this to be in the conll format
	posTags = {}
	linenum = 0
	wordnum = 0
	posTags[0] = defaultdict(str)
	for line in inputFile:
		if line == "\n" or len(line.split()) <= 0:
			linenum+=1
			posTags[linenum] = defaultdict(str)
			wordnum = 0
		else:
			posTags[linenum][wordnum] = line.split()[1]
			wordnum+=1
	return posTags

posTagsFile = open("posFile.txt","r")
posTags = seedPOS(posTagsFile)

print "Obtained POS Tags"


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

def posTagsPresent(posTags, num, pos, inputFile):
	for line in inputFile:
		if (posTags[num][pos] == line.split()[0]) and (posTags[num][pos] == line.split()[1]) and (posTags[num][pos] == line.split()[2]):
			return True
	return False

#Update: Added the POS tagging in this step as well as I keep track of all the info required for that in this method itself.
def extractngramspos(inputFile,seed_word):
	unigram = list()
	bigram = list()
	trigram = list()
	num = 0
	pos = 0	
	prevword = ""
	numword = 0
	for line in inputFile:
		pos = extractWordPos(seed_word,line.strip(),1)
		#Add the unigram POS tag check here

		if pos!=-1 and line[pos]!=seed_word:
			if posTags[num][pos] == "V":
				unigram.append(line.split()[pos]) 
			try:
				if (posTags[num][pos] == "V" and posTags[num][pos+1] == "V") or (posTags[num][pos] == "V" and posTags[num][pos+1] == "R") or (posTags[num][pos] == "R" and posTags[num][pos+1] == "V") or (word == "to" and posTags[num][pos+1] == "V") or (posTags[num][pos] == "V" and posTags[num][pos+1] == "N") or (posTags[num][pos] == "V" and posTags[num][pos+1] == "A") or (posTags[num][pos] == "V" and posTags[num][pos+1] == "O") :
					bigram.append(line.split()[pos]+ " "+line.split()[pos+1])
			except:
				asdf = 0
		
			try:
				if posTagsPresent(posTags,num,pos,open("trigram_rules.txt","r")):
					trigram.append(line.split()[pos] + " "+line.split()[pos+1] + " "+line.split()[pos+2])
			except:
				asdf = 0
		num +=1
	return [unigram,bigram,trigram]

#EXtracting n grams before the word - for negative

def extractngramsneg(inputFile,seed_word):
	unigram = list()
	bigram = list()
	num = 0
	pos = 0	
	prevword = ""
	numword = 0
	for line in inputFile:
		pos = extractWordPos(seed_word,line.strip(),0)
		if pos!=-1 and line[pos]!=seed_word:
			if posTags[num][pos] == "V":
				unigram.append(line.split()[pos])
			try:
				if (posTags[num][pos-1] == "V") or (posTags[num][pos-1] == "R") or (posTags[num][pos] == "R" and posTags[num][pos-1] == "V"):
					bigram.append(line.split()[pos-1] + " "+line.split()[pos])
			except:
				asdf = 1
		num +=1
	return [unigram,bigram]

#To calculate the score for negative sentiment
def calculateScorepos(poswords, phrase, posFile, negFile):
	numofgrams = len(phrase.split())
	poswordslist = list(poswords)
	countpos = 0
	countneg = 0
	for line in posFile:
		for word in poswordslist:
			pos = extractWordPos(word,line.strip(),1)
			if pos!=-1:																#To check if the positive word is in the line and put the pointer after that
				try:
					if line.split()[pos:pos+numofgrams] == phrase.split():			#To check if the positive word is before the negative word
						countpos +=1
				except:
					countpos+=0
	pos =0
	for line in negFile:
		for word in poswordslist:
			pos = extractWordPos(word,line.strip(),1)
			if pos!=-1:
				try:
					if line.split()[pos:pos+numofgrams] == phrase.split():
						countneg +=1
				except:
					countneg+=0
	if countpos == 0 and countneg == 0:
		return 0
	if (countpos+countneg) <=4:
		return 0
	return float(float(countpos)/(float(countneg)+float(countpos)))

#To calculate the score for positive words using negative words
def calculateScoreneg(negwords, phrase, posFile, negFile):
	numofgrams = len(phrase.split())
	negwordslist = list(negwords)
	countpos = 0
	countneg = 0
	for line in posFile:
		for word in negwordslist:								#Added to check if the positive word occurs before a negative phrase not THE negative phrase
			pos = extractWordPos(word,line.strip(),0)
			if pos!=-1:											#To check if the negative word is in the line
				try:
					if line.split()[pos-numofgrams+1:pos+1] == phrase.split():		#To check if the positive word is before the negative word
						countpos +=1
				except:
					countpos+=0
	pos =0
	for line in negFile:
		for word in negwordslist:
			pos = extractWordPos(word,line.strip(),0)
			if pos!=-1:
				try:
					if line.split()[pos-numofgrams+1:pos+1] == phrase.split():
						countneg +=1
				except:
					countneg+=0

	if countpos == 0 and countneg == 0:
		return 0
	if (countpos+countneg) <=4:
		return 0
	return float(float(countpos)/(float(countneg)+float(countpos)))

def generateAllCombos (word):
	if len(word.split())> 1:
		return word.split()+[i[0] +" "+ i[1] for i in zip(word.split(),word.split()[1:])]
	else:
		return word.split()

def subsumed(word, wordset):
	l = list(wordset)
	numofgrams = len(word.split())
	l1 = l  						#For holding the length of the list
	wordlist = generateAllCombos(word)
	for num in xrange(len(l)):
		if l[num] in wordlist or word==l[num]:
			return True

	return False	

def stemWords(line):
	line1 = ""
	for word in line.split():
		line1 = line1 +" "+st.stem(word)
	return line1

def extractPredicates(negative_seed_word, inputFile)	:
	copulae = open("copulae.txt","r")
	copularVerbs = list()
	unigram = list()
	bigram = list()
	trigram = list()
	num = 0
	for lines in copulae:
		copularVerbs.append(lines)
	for line in inputFile:
		for word in copularVerbs:
			pos = extractWordPosPredicate(word.strip(),line.strip(),1)			#added inflections here; pointer points to the location right after the copular verb
			if pos!=-1:														#Copular verb found
				pos1 = extractWordPos(negative_seed_word,line.strip(),0)		#see if the negative word is there
				if pos1!=-1:
					pos1+=1  												#the pointer now points to the negative word
					numofgram = len(negative_seed_word.split())
					pos1end = pos1+numofgram   								#the pointer points to the end of then negative word	
					if abs(pos - pos1) <=5 or abs(pos - pos1end)<=5:			#sees if the word after the inflection verb is less than 5 grams from the negative word
						if posTags[num][pos] == "A":
							unigram.append(line.split()[pos])
				
						if (posTags[num][pos] == "A" and posTags[num][pos+1] == "R") or (posTags[num][pos] == "R" and posTags[num][pos+1] == "A") or (posTags[num][pos] == "A" and posTags[num][pos+1] == "N"):
							bigram.append(line.split()[pos]+" "+line.split()[pos+1])
				
						if (posTags[num][pos] == "R" and posTags[num][pos] == "A" and posTags[num][pos] == "N") or (posTags[num][pos] == "D" and posTags[num][pos] == "A" and posTags[num][pos] == "N"):
							trigram.append(line.split()[pos]+" "+line.split()[pos+1]+" "+line.split()[pos+2])

		num+=1
	return [unigram,bigram,trigram]


#To calculate the score for positive predicates using negative words
def calculateScorePredicates(negwords, phrase, posFile, negFile):
	numofgrams = len(phrase.split())
	negwordslist = list(negwords)
	countpos = 0
	countneg = 0
	for line in posFile:
		for word in negwordslist:
			pos = extractWordPos(word,line.strip(),0)
			pos1 = extractWordPos(phrase,line.strip(),0)
			if pos!=-1 and pos1!=-1:
				pos+=1
				pos1+=1
				pos1end = pos1+numofgrams
				try:
					if abs(pos - pos1) <=5 or abs(pos - pos1end)<=5:
						countpos +=1
				except:
					countpos+=0
	pos =0
	for line in negFile:
		for word in negwordslist:							#for all words in the negative word list
			pos = extractWordPos(word,line.strip(),0)				#FInd if the negative word is there in the sentence
			pos1 = extractWordPos(phrase,line.strip(),0)		#Find if the positive predicate is in the sentence
			if pos!=-1 and pos1!=-1:
				pos+=1  										#Mark the starting postions of the sentence
				pos1+=1   										
				pos1end = pos1+numofgrams   					
				try:
					if abs(pos - pos1) <=5 or abs(pos - pos1end)<=5:  				#See distance no need to take copular verbs here because we already have th phrase we want to check with
						countneg +=1
				except:
					countneg+=0

	if countpos == 0 and countneg == 0:
		return 0
	return float(float(countpos)/(float(countneg)+float(countpos)))


seedword = "love"
positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
positivewords = set()
negativewords = set()
predicatewords = set()
prevpositivewords = set()
positivewords.add(seedword)
iteratenum = 1
print "Started Bootstrapping"
while len(positivewords - prevpositivewords) > 0:
	positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
	negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
	triedwords = set()
	check = positivewords
	prevpositivewords = set(positivewords)  			#TO check for convergence
	score = defaultdict(float)
	print "Collecting negative words"
	while len(check - triedwords) > 0:
		seed_word = list(check - triedwords)[0]
		triedwords.add(seed_word)
		ngrams = extractngramspos(positiveFile,seed_word)	#For negative words -- returns step 1 and step 2 also

		unigram = ngrams[0]
		bigram = ngrams[1]
		trigram = ngrams[2]
	
		print "for ",seed_word
		for x in xrange(len(unigram)):
			#print unigram[x]
			positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
			negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
			score[unigram[x]] = calculateScorepos(positivewords,unigram[x],positiveFile, negativeFile)
	
		for x in xrange(len(bigram)):
			positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
			negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
			score[bigram[x]] = calculateScorepos(positivewords,bigram[x],positiveFile, negativeFile)
		for x in xrange(len(trigram)):
			positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
			negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
			score[trigram[x]] = calculateScorepos(positivewords,trigram[x],positiveFile, negativeFile)
	
	sorted_score = sorted(score.iteritems(), key = operator.itemgetter(1))[::-1]

	print "Score of negative words"
	print sorted_score
	numofwords = 0
	countnotsubwords = 0
	for numofwords in xrange(len(sorted_score)):
		if not subsumed(sorted_score[numofwords][0],negativewords) and sorted_score[numofwords][1] > 0.5:	
			countnotsubwords+=1		#Check if the words are subsumed already in the negative words class
			negativewords.add(sorted_score[numofwords][0])
		if countnotsubwords == 20:
			break

	print "\n\nnegative words",negativewords
	print "***********************************\n\n"


	triedwords = set()
	check = negativewords
	score = defaultdict(float)
	print "Collecting Positive words"
	while len(check - triedwords) > 0:
		seed_word = list(check - triedwords)[0]
		triedwords.add(seed_word)
		positiveFile = open("positiveTweets.txt","r")		#Gets the negative instances of sarcasm
		ngrams = extractngramsneg(positiveFile,seed_word)	#For negative words -- returns step 1 and step 2 also

		unigram = ngrams[0]
		bigram = ngrams[1]

		print "for ",seed_word

		for x in xrange(len(unigram)):
			positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
			negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
			score[unigram[x]] = calculateScoreneg(negativewords,unigram[x],positiveFile, negativeFile)
		
		for x in xrange(len(bigram)):
			positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
			negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
			score[bigram[x]] = calculateScoreneg(negativewords,bigram[x],positiveFile, negativeFile)
	
	
	sorted_score = sorted(score.iteritems(), key = operator.itemgetter(1))[::-1]
	print "Score of positive words"
	print sorted_score
	numofwords = 0
	countnotsubwords = 0
	for numofwords in xrange(len(sorted_score)):
		if countnotsubwords <=10 and sorted_score[numofwords][1] > 0.5:									#Taking the top 20
			if not subsumed(sorted_score[numofwords][0],positivewords):				#Check if the words are subsumed already in the negative words class
				countnotsubwords+=1
				positivewords.add(sorted_score[numofwords][0])

	print "\npositive words",positivewords
	print "***********************************\n"

	print "Collecting predicates"
	triedwords = set()
	check = negativewords
	score = defaultdict(float)
	while len(check - triedwords) > 0:
		seed_word = list(check - triedwords)[0]
		triedwords.add(seed_word)
		positiveFile = open("positiveTweets.txt","r")		#Gets the negative instances of sarcasm
		ngrams = extractPredicates(seed_word,positiveFile)	#For negative words -- returns step 1 and step 2 also

		unigram = ngrams[0]
		bigram = ngrams[1]
		
		print "for ",seed_word

		for x in xrange(len(unigram)):
			positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
			negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
			score[unigram[x]] = calculateScorePredicates(negativewords,unigram[x],positiveFile, negativeFile)
		
		for x in xrange(len(bigram)):
			positiveFile = open("positiveTweets.txt","r")		#Gets the Positive instances of sarcasm
			negativeFile = open("negativeTweets.txt","r")		#Gets the negative instances of sarcasm
			score[bigram[x]] = calculateScorePredicates(negativewords,bigram[x],positiveFile, negativeFile)
		
	
	sorted_score = sorted(score.iteritems(), key = operator.itemgetter(1))[::-1]
	print "Score of predicate words"
	print sorted_score
	numofwords = 0
	countnotsubwords = 0
	for numofwords in xrange(len(sorted_score)):
		if countnotsubwords <=10:									#Taking the top 20
			if not subsumed(sorted_score[numofwords][0],predicatewords):				#Check if the words are subsumed already in the negative words class
				predicatewords.add(sorted_score[numofwords][0])
				countnotsubwords+=1
		else:
			break

	print "\npredicate words",predicatewords
	print "***********************************\n"

	print "iteration complete ",iteratenum
	iteratenum+=1

for word in positivewords:
	with open("positivewords.txt","a") as myFile:
		myFile.write(word+"\n")
for word in negativewords:
	with open("negativewords.txt","a") as myFile:
		myFile.write(word+"\n")
for word in predicatewords:
	with open("positivepredicatewords.txt","a") as myFile:
		myFile.write(word+"\n")

