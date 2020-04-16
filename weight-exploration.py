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


debug_card = 'UFC_187'


def find_only_whole_word(search_string, input_string):
  # Create a raw string with word boundaries from the user's input_string
  raw_search_string = r"\b" + search_string + r"\b"

  match_output = re.search(raw_search_string, input_string)
  ##As noted by @OmPrakesh, if you want to ignore case, uncomment
  ##the next two lines
  match_output = re.search(raw_search_string, input_string, 
                           flags=re.IGNORECASE)

  no_match_was_found = ( match_output is None )
  if no_match_was_found:
    return False
  else:
    return True    

def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    

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
    
    for s in text_spacy.split('. '):
        for p in trigger_phrases:
            if p in s:
                possible_misses.append(s)


    print()
    print()
    print("Possible Misses:")
    print(possible_misses)


    fight_df = pd.read_csv(df_path + ff + '.csv')
    
    #print(fight_df)
    
    #Create a list of fighter names from the fight_df
    fighter_list_winner = fight_df['winner'].values.tolist()
    fighter_list_loser = fight_df['loser'].values.tolist()
    fighter_list = fighter_list_winner + fighter_list_loser

    print()
    print()
    print("Fighter List:")
    for f in fighter_list:
        print(f)

    fighter = ""
    weight = ""
    possible_weight = ""
    
    all_stopwords = nlp.Defaults.stop_words
    weight_sigs = ["lb", "lbs", "pound", "pounds", "lb.", "lbs."]
    
    for possible_miss in possible_misses:
        for word in possible_miss.split():
            #OK here we are going to check to see if the word is in
            #the list of fighters.
            for f in fighter_list:
                for f_split in f.split():
                    #                print(find_only_whole_word(f, word))
#                        if (find_only_whole_word(f_split, word)):
#                            print(f"{f}: {word}")
                        if (find_only_whole_word(f_split, word)):
                            fighter = f
                            #print(f"{f} matches {word}")
            #Find the number:
            #print(word)
            if isfloat(word):
                possible_weight = word
            elif possible_weight != "":
                if word in weight_sigs:
                    weight = possible_weight
                    possible_weight = ""
                else:
                    possible_weight = ""
                
    print()
    print()
    print("Final Result:")
    if fighter != "":
        if weight != "":
            print(f"{fighter} weighed in at {weight} at {ff}")

    
missed_weight_debug(debug_card)

