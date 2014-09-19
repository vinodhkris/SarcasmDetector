SarcasmDetector
===============

Authors : Vinodh Krishnan, Vivek Nabhi : Georgia Institute of Technology, Atlanta

This is a Sarcasm Detector we built for CS 7650 Natural Language Processing Final Project. We start off by implementing a state of the art method, then we try to make that better and try to implement another method to compare if necessary. 

First off we start by implementing this Sarcasm paper that uses context from EMNLP 2013 - www.cs.utah.edu/~huangrh/official-sarcasm-cameraReady-v2.pdf

3 phases

1. Bootstrapping positive sentiments and negative situations  
2. Adding positive predicates.  
3. Implementing SVM with unigram and bigram features, so that we can plug in both of them.  

The code for the first 2 phases can be found at SaracasmDetector-Part1 folder in the current git repo. The recall achieved was 9.7 and the Precision was 72.4. We used SVM with a multitude of features (unigram, bigram, author, tweet length, etc) to increase the recall and achieve a fmeasure of 62, which is better than that proposed by the paper. 



