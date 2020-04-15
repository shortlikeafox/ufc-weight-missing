# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy
import re

#What we want to do is find if fighters missed weight! 

#We have a test set of all of 2019 so we will use that, but train on 
#other data.  
#We can find 
#some at: https://www.betmma.tips/ufc_fighters_who_missed_weight.php

my_path = 'fight-page-dump/'
df_path = 'fight-dataframes/'


debug_card = 'The_Ultimate_Fighter_5_Finale'

def missed_weight_debug(ff):
    fight_file=open(my_path + ff, "r")
    
    bs=BeautifulSoup(fight_file.read(), 'html.parser')
    text_no_html = bs.text
    
    print("wiki dump:")
    print(bs)
    
    import spacy
    
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    
    doc=nlp(text_no_html)
    
    text_spacy = " ".join([token.lemma_ for token in doc])

    print()
    print()
    print("Lemmatized with spacy")
    print(text_spacy)

    #I like the spacy text better.
    #Let's isolate the sentence where the fighter misses weight
    trigger_phrases = ['miss weight']
    possible_misses = []
    
    for s in text_spacy.split('. | ,'):
        for p in trigger_phrases:
            if p in s:
                possible_misses.append(s)


    print()
    print()
    print("Possible Misses:")
    print(possible_misses)


missed_weight_debug(debug_card)