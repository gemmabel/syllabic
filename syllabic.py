# -*- coding:utf-8 -*-
import re
import os
import pyphen


class SyllableStatistics(object):
    
    def __init__(self, corpus_path, lang_code='es_MX'):
        
        lang = pyphen.language_fallback(lang_code)
        
        self.dic = pyphen.Pyphen(lang=lang)
        self.freqs = {}
        
        for root, _, files in os.walk(corpus_path):
            for filepath in files:
                with open(root + "/" + filepath, "r") as f:
                    content = f.read()
                
                tokens = self.tokenize(content)
                for token in tokens:
                    result = self.dic.inserted(token).split("-")
                    for syllable in result:
                        try:
                            self.freqs[syllable] += 1
                        except:
                            self.freqs[syllable] = 1
                continue
            import ipdb;ipdb.set_trace()
    
    def tokenize(self, text):
        temp_text = re.sub(r'[^\w\s]', 
                           '', 
                           text, 
                           re.UNICODE).lower()
        temp = temp_text.split(" ")
        while '' in temp:
            temp.remove('')
        return temp
    
    
#lang = pyphen.language_fallback('es_MX')
#dic = pyphen.Pyphen(lang=lang)