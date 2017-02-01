#!/usr/bin/env python3
# Based on Mabodo's ipython notebook (https://github.com/mabodo/sibilizador)
# (c) Mabodo

import re

class char():
    def __init__(self):
        pass
    
class char_line():
    def __init__(self, word):
        self.word = word
        self.char_line = [(char, self.char_type(char)) for char in word]
        self.type_line = ''.join(chartype for char, chartype in self.char_line)
        
    def char_type(self, char):
        if char in set(['a', 'á', 'e', 'é','o', 'ó', 'í', 'ú']):
            return 'V' #strong vowel
        if char in set(['i', 'u', 'ü']):
            return 'v' #week vowel
        if char=='x':
            return 'x'
        if char=='s':
            return 's'
        else:
            return 'c'
            
    def find(self, finder):
        return self.type_line.find(finder)
        
    def split(self, pos, where):
        return char_line(self.word[0:pos+where]), char_line(self.word[pos+where:])
    
    def split_by(self, finder, where):
        split_point = self.find(finder)
        if split_point!=-1:
            chl1, chl2 = self.split(split_point, where)
            return chl1, chl2
        return self, False
     
    def __str__(self):
        return self.word
    
    def __repr__(self):
        return repr(self.word)

class Syllabificator():
    def __init__(self):
        self.grammar = []
        
    def split(self, chars):
        rules  = [('VV',1), ('cccc',2), ('xcc',1), ('ccx',2), ('csc',2), ('xc',1), ('cc',1), ('vcc',2), ('Vcc',2), ('sc',1), ('cs',1),('Vc',1), ('vc',1), ('Vs',1), ('vs',1)]
        for split_rule, where in rules:
            first, second = chars.split_by(split_rule,where)
            if second:
                if first.type_line in set(['c','s','x','cs']) or second.type_line in set(['c','s','x','cs']):
                    #print 'skip1', first.word, second.word, split_rule, chars.type_line
                    continue
                if first.type_line[-1]=='c' and second.word[0] in set(['l','r']):
                    continue
                if first.word[-1]=='l' and second.word[-1]=='l':
                    continue
                if first.word[-1]=='r' and second.word[-1]=='r':
                    continue
                if first.word[-1]=='c' and second.word[-1]=='h':
                    continue
                return self.split(first)+self.split(second)
        return [chars]
        
    def __call__(self, word):
        return self.split(char_line(word))
    
class Syllabicator(object):
    
    def __init__(self):
        '''http://ponce.inter.edu/acad/cursos/ciencia/lasvi/modulo2.htm'''
        
        vocal_fuerte = ["a", "e", "o", "í", "ú"]
        vocal_debil = ["i", "u"]
        
        diptongos_crecientes = ["ie", "ia", "io", "ua", "ue", "uo"]
        diptongos_decrecientes = ["ai", "ei", "oi", "ay", "ey", "oy", "au", 
                                  "eu", "ou"]
        diptongos_homogeneos = ["iu", "ui"]
        diptongos = diptongos_crecientes + \
                    diptongos_decrecientes + \
                    diptongos_homogeneos
        self.v_diptongo = re.compile(r"|".join(diptongos))
        
        triptongos_i = ["iau", "iai", "uai", "uau", "ieu", "iei", "iay", 
                        "uay", "iey"]
        triptongos_u = ["uei", "ueu", "iou", "ioi", "uoi", "uou", "uey", 
                        "ioy", "uoy"]
        triptongos = triptongos_i + triptongos_u
        self.v_triptongo = re.compile(r"|".join(triptongos))
        
        grupos_inseparables = ["br", "cr","dr", "gr", "fr", "kr", "tr", "bl", 
                               "cl", "gl", "fl", "kl", "pl", "tl"]
        self.c_inseparables = re.compile(r"|".join(grupos_inseparables))
        
                            
        # Una consonante entre dos vocales se agrupa con la vocal de la derecha:
        self.vcv = re.compile("")
        
        # Dos consonantes entre dos vocales se separan y cada consonante se queda con una vocal:
        
        # ¡Atención! Si la segunda consonante es r o l, las dos consonantes se agrupan con la segunda vocal.
        
        # Cuando hay tres consonantes entre vocales, las primeras dos se unen con la primera vocal y la tercera se une a la segunda vocal.
        
        # Excepción: Si la tercera consonante es r o l, la primera consonante se une con la primera vocal y las otras dos con la siguiente.
        
        # Cuando hay cuatro consonantes entre vocales, las primeras dos se unen a la primera vocal y las otras dos se unen a la segunda vocal.
        
        # Recuerda que las consonantes dobles: ch, ll, rr representan un solo fonema, por lo que para efectos de la división silábica cuentan como una sola consonante (no se separan). Se aplica entonces la regla #1.
    
        pass
        
    
    def __call__(self, word):
        lower_word = word.lower()
        