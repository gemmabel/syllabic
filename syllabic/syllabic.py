# -*- coding:utf-8 -*-
import re
import os
import string
import pyphen
import nltk
from syllabificator import Silabicador
from unidecode import unidecode


class SyllableStatistics(object):
    
    def __init__(self, corpus_path, lang_code='es_MX'):
        
        lang = pyphen.language_fallback(lang_code)
        
        self.dic = pyphen.Pyphen(lang=lang)
        self.freqs = {}
        
        self.syllabificator = Syllabificator()

        for root, _, files in os.walk(corpus_path):
            for filepath in files:
                with open(root + "/" + filepath, "r") as f:
                    content = f.read()
                
                tokens = self.tokenize(content)
                sentences = self.sentences(content)
                readability = self.readability(content)
                for token in tokens:
                    result = self.syllabificator(token)
#                     try:
#                         print("-".join([str(res) for res in result]))
#                     except:
#                         import ipdb;ipdb.set_trace()
#                         exit(0)
                    for syllable in result:
                        syllable = unidecode(str(syllable))
                        if syllable == "rnu":
                            import ipdb;ipdb.set_trace()
                        try:
                            self.freqs[syllable] += 1
                        except:
                            self.freqs[syllable] = 1
                continue
            
            import ipdb;ipdb.set_trace()
    
    def readability(self, text):
        # Lecturabilidad / Índice Fernández Huerta = 206,84-(60 x (S / P) – (1,02 x (P / F)
        # S = Sílabas, P = Palabras, F =Frases.
        # (60 x S / P) es lo mismo como 0,60 x S si tomamos ejemplos de 100 palabras.
        
        # “F” realmente debería ser el promedio de palabras por frase, 
        # como en la fórmula de Flesch. En el texto de la “Revista Española de 
        # Salud Pública” se escribe al final que el índice de la fórmula 
        # Fernández-Huerta para su propio texto es de 64,96. Este valor solo se 
        # puede lograr si “F” es el promedio de palabras por frase 
        # (sino sale un valor de legibilidad de 98).
        # https://seo-quito.com/seo-legibilidad-flesch-szigriszt-fernandez-huerta/
        
        # Índice de perspicuidad de Szigriszt-Pazos
        # IPSP = 206.835 - (62.3 * (S/P)) - (P/F)
        # IPSP es la perspicuidad; 
        # S, el total de sílabas; 
        # P, la cantidad de palabras; 
        # F, el número de frases.
        
        tokens = self.tokenize(text)
        sentences = self.sentences(text)
        S = 0
        for token in tokens:
            S += len(self.syllabificator(token))
            
        P = len(tokens)
        F = len(sentences)
        return 206.835 - (62.3 * (S/P)) - (P/F)
    
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
            
#lang = pyphen.language_fallback('es_MX')
#dic = pyphen.Pyphen(lang=lang)