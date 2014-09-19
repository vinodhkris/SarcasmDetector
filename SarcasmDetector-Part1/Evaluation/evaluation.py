file1 = open("resultsFile.txt","r")
file2 = open("test.tag","r")
tp = 0
fp = 0
fn = 0
tn = 0
for word in zip(file1,file2):

	if word[0].strip() == word[1].strip() and word[0].strip() == "SARCASM":
		tp+=1
	elif word[0].strip() == "SARCASM":
		fp+=1
	elif word[1].strip() == "SARCASM":
	 	fn+=1
	else:
		tn+=1

try:
	print "Precision ",float(tp)/(float(tp) + float(fp))
	print "Recall", float(tp)/(float(tp)+float(fn))
except:
	print "Precision",0
	print "Recall",0
