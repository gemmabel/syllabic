#!/usr/bin/env python3
# Based on Mabodo's ipython notebook (https://github.com/mabodo/sibilizador)
# (c) Mabodo

import re

class Char(object):
    
    def __init__(self, pattern, char_type, interval):
        self.char_type = char_type
        self.pattern = pattern
        self.interval = interval
        

class CharArray(object):
    
    def __init__(self, word):
        if not isinstance(word, str):
            raise TypeError("No the correct type for a char array")
        
        self.vocales_fuertes = ["a", "e", "o", "á", "é", "ó", "í", "ú"]
        self.vocales_debiles = ["i", "u"]
        self.vocales = self.vocales_debiles + self.vocales_fuertes

        self.consontant_y = ["y" + vowel for vowel in self.vocales]
        
        diptongos_crecientes = [d + f for d in self.vocales_debiles\
                                      for f in self.vocales_fuertes]
        #diptongos_crecientes = ["ie", "ia", "io", "ua", "ue", "uo",
        #                        "ié", "iá", "ió", "uá", "ué", "uó"]
        #diptongos_decrecientes = ["ai", "ei", "oi", "ay", "ey", "oy", "au", 
        #                          "eu", "ou", "ái", "éi", "ói", "áy", "éy", 
        #                          "óy", "áu", "éu", "óu"]
        diptongos_decrecientes = [f + d for d in self.vocales_debiles\
                                        for f in self.vocales_fuertes] + \
                                 [f + "y" for f in self.vocales_fuertes]
        diptongos_homogeneos = ["iu", "ui"]
        self.diptongos = diptongos_crecientes + \
                         diptongos_decrecientes + \
                         diptongos_homogeneos
        
        #triptongos_i = set({"iau", "iai", "uai", "uau", "ieu", "iei", "iay", 
        #                "uay", "iey"})
        #triptongos_u = set({"uei", "ueu", "iou", "ioi", "uoi", "uou", "uey", 
        #                "ioy", "uoy"})
        self.triptongos = [dip + d for dip in diptongos_crecientes \
                                   for d in self.vocales_debiles] +\
                          [dip + "y" for dip in diptongos_crecientes]
                
        self.grupos_inseparables = ["br", "cr","dr", "gr", "fr", "kr", "tr", "bl", 
                                    "cl", "gl", "fl", "kl", "pl", "tl", "ll", "ch",
                                    "rr"]
        
        self.word = word
        self.vocal_representation = self.build_abstract_representation(word)
        
    def build_abstract_representation(self, word):
        representation = {}
        
        for consonant_y in self.consontant_y:
            while consonant_y in word:
                word = word.replace("y", "#", 1)
        
        for triptongo in self.triptongos:
            while triptongo in word:
                beginning = word.index(triptongo)
                end = beginning + len(word)
                interval = (beginning, end)
                representation[triptongo] = representation.get(triptongo, 
                                                               []).append(
                                                                   interval)
                word = word.replace(triptongo, "@", 1)
                
        for diptongo in self.diptongos:
            while diptongo in word:
                beginning = word.index(diptongo)
                end = beginning + len(word)
                interval = (beginning, end)
                representation[diptongo] = representation.get(diptongo, 
                                                               []).append(
                                                                   interval)
                word = word.replace(diptongo, "@", 1)
                
        for grupo_c in self.grupos_inseparables:
            while grupo_c in word:
                beginning = word.index(grupo_c)
                end = beginning + len(word)
                interval = (beginning, end)
                representation[grupo_c] = representation.get(grupo_c, 
                                                             []).append(
                                                                   interval)
                word = word.replace(grupo_c, "#", 1)
                
        for vowel in self.vocales_debiles:
            while vowel in word:
                word = word.replace(vowel, "|", 1)
                
        for vowel in self.vocales_fuertes:
            while vowel in word:
                word = word.replace(vowel, "@", 1)
                
        for consonant in list("bcdfghjklmnñpqrstvwxyz"):
            while consonant in word:
                word = word.replace(consonant, "#", 1)
                
        word = word.replace("#", "C").replace("@", "V").replace("|", "V")
        return word
    
    def unmask(self, pattern):
        result = []
        word = self.word
        for syllable in pattern:
            subsyl = ""
            for character in syllable:
                found = False
                if character == "C":
                    if len(word) > 1 and\
                       word[1] in "bcdfghjklmnñpqrstvwxyz" and not found:
                        for grupo_c in self.grupos_inseparables:
                            if word.startswith(grupo_c):
                                subsyl += grupo_c
                                word = word[2:]
                                found = True
                                break
                    if not found:
                        subsyl += word[0]
                        word = word[1:]
                elif character == "V":
                    if len(word) > 2 and \
                       word[1] in self.vocales and word[2] in self.vocales:
                        for triptongo in self.triptongos:
                            if word.startswith(triptongo):
                                subsyl += triptongo
                                word = word[3:]
                                found = True
                                break
                    if len(word) > 1 and \
                       word[1] in self.vocales and not found:
                        for diptongo in self.diptongos:
                            if word.startswith(diptongo):
                                subsyl += diptongo
                                word = word[2:]
                                found = True
                                break
                    if not found:
                        subsyl += word[0]
                        word = word[1:]
            result.append(subsyl)
        return result
    
    def __str__(self, *args, **kwargs):
        return str(self.vocal_representation)
    
    def __repr__(self, *args, **kwargs):
        return str(self)
    
class Silabicador(object):
    
    def __call__(self, word):
        '''http://ponce.inter.edu/acad/cursos/ciencia/lasvi/modulo2.htm'''
        
        res = []
        lower_word = word.lower()
        char_array = CharArray(lower_word)
        abstract_word = list(str(char_array))
        
        while len(abstract_word) != 0:
            if abstract_word[0] == "V":
                if len(abstract_word) == 1:
                    res += ["V"]
                    abstract_word = []
                elif len(abstract_word) == 2:
                    if abstract_word[1] == "C":
                        res += ["VC"]
                    else:
                        res += ["V", "V"]
                    abstract_word = []
                elif len(abstract_word) == 3:
                    res += ["V", "CV"]
                    abstract_word = []
                else:
                    # Una consonante entre dos vocales se agrupa con la vocal de la derecha:
                    if abstract_word[1] == "C" and\
                       abstract_word[2] == "V":
                        res += ["V", "CV"]
                        del abstract_word[2]
                        del abstract_word[1]
                        del abstract_word[0]
                    # Dos consonantes entre dos vocales se separan y cada consonante se queda con una vocal:
                    elif abstract_word[1] == "C" and\
                       abstract_word[2] == "C" and\
                       abstract_word[3] == "V":
                        res += ["VC", "CV"]
                        del abstract_word[3]
                        del abstract_word[2]
                        del abstract_word[1]
                        del abstract_word[0]
                        
                    # Cuando hay tres consonantes entre vocales, las primeras dos se unen con la primera vocal y la tercera se une a la segunda vocal.
                    elif abstract_word[1] == "C" and\
                         abstract_word[2] == "C" and\
                         abstract_word[3] == "C" and\
                         abstract_word[4] == "V":
                        res += ["VCC", "CV"]
                        del abstract_word[4]
                        del abstract_word[3]
                        del abstract_word[2]
                        del abstract_word[1]
                        del abstract_word[0]
                    # Cuando hay cuatro consonantes entre vocales, las primeras dos se unen a la primera vocal y las otras dos se unen a la segunda vocal.
                    elif abstract_word[1] == "C" and\
                         abstract_word[2] == "C" and\
                         abstract_word[3] == "C" and\
                         abstract_word[4] == "C" and\
                         abstract_word[5] == "V":
                        res += ["VCC", "CCV"]
                        del abstract_word[5]
                        del abstract_word[4]
                        del abstract_word[3]
                        del abstract_word[2]
                        del abstract_word[1]
                        del abstract_word[0]
            elif abstract_word[0] == "C":
                res.append(abstract_word.pop(0))

        final_grouping = []
        while len(res)>0:
            if res[0] == "C" and \
               len(res) != 1 and \
               res[1].startswith("V"):
                final_grouping.append(res[0] + res[1])
                del res[1]
                del res[0]
            elif res[0] == "C": # La consonante pega con la silaba anterior
                final_grouping[-1] = final_grouping[-1] + res[0]
                del res[0]
            else:
                final_grouping.append(res[0])
                del res[0]
        
        return char_array.unmask(final_grouping), final_grouping