import json
import ast
from collections import defaultdict

def processJson(inputFileName,outputFileName):
	lines = defaultdict(str)
	num=0
	with open(inputFileName) as input:
		for line in input:
			data = ast.literal_eval(line.strip("\n").encode('utf-8'))
			lines[num] = ""
			for line in data['text']:
				lines[num]+= line.strip("\n").encode('utf-8')
			num+=1

	for num in lines:
		with open(outputFileName,"a") as myFile:
			myFile.write(str(lines[num])+"\n")
#return lines

processJson("positive.json","positiveTweets.txt")
processJson("negative.json","negativeTweets.txt")