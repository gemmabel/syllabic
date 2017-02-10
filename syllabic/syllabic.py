# -*- coding:utf-8 -*-
import re
import os
import string
import nltk
from syllabicator import Silabicador
from unidecode import unidecode
from collections import OrderedDict
import numpy as np


class Tokenizer(object):
    
    def unique_chars(self, text):
        chars = set(list(text))
        return chars
    
    def remove_punctuation(self, text):
        spanish_punctuation = "¡!“-,¿.?,…\xa0\xad–—\n«»”"
        return re.sub('[%s]' % re.escape(spanish_punctuation + string.punctuation), ' ', text)
    
    def sentences(self, text):
        spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        return spanish_tokenizer.tokenize(text)
    
    def tokenize(self, text):
        temp_text = self.remove_punctuation(text)
        temp_text = re.sub('\d+', # No numbers
                           '',
                           temp_text,
                           re.UNICODE).lower()
        temp_text = re.sub(r'[^\w\s]', 
                           '', 
                           temp_text, 
                           re.UNICODE).lower()
        
        temp = temp_text.split(" ")
        while '' in temp:
            temp.remove('')
        return temp
    
    def tokenize_sentences(self, sentences):
        res = []
        for sentence in sentences:
            res.append(self.tokenize(sentence))
            

class SyllableStatistics(Tokenizer):
    
    def __init__(self, corpus_path, with_accents=False):
        
        self.freqs = {}
        self.readable = {}
        self.syllabificator = Silabicador()
        
        total_syllables = 0

        for root, _, files in os.walk(corpus_path):
            for filepath in files:
                with open(root + "/" + filepath, "r") as f:
                    content = f.read()
                
                tokens = self.tokenize(content)
                sentences = self.sentences(content)
                for token in tokens:
                    result = self.syllabificator(token)
#                     try:
#                         print("-".join([str(res) for res in result]))
#                     except:
#                         import ipdb;ipdb.set_trace()
#                         exit(0)
                    for syllable in result:
                        syllable = str(syllable)
                        if not with_accents:
                            syllable = unidecode(syllable)
                            
                        try:
                            self.freqs[syllable] += 1
                        except:
                            self.freqs[syllable] = 1
                        total_syllables += 1
                print(filepath)
        
        self.freqs = OrderedDict(sorted(self.freqs.items(), 
                                        key=lambda x:x[1],
                                        reverse=True)
                                 )
        
        self.readable = OrderedDict(sorted(self.readable.items(),
                                           key=lambda x:x[1],
                                           reverse=True)
                                    )
        
        # Calculate probabilities
        probabilities = {}
        for syl, freq in self.freqs.items():
            probabilities[syl] = freq/total_syllables
            
        self.probabilities = np.array(sorted(probabilities.items()))
        self.syls = np.array(self.probabilities[:,0])
        self.proba = np.array(self.probabilities[:,1], dtype=np.float64)
    
    
    def generate_samples(self, n):
        return np.random.choice(self.syls,
                                n,
                                p=self.proba)