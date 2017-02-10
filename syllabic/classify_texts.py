# -*- coding:utf-8 -*-

# 0 a 15    muy difícil    científica, filosófica    titulados universitarios
# 16 a 35    árido    pedagógica, técnica    selectividad y estudios universitarios
# 36 a 50    bastante difícil    literatura y divulgación    cursos secundarios
# 51 a 65    normal    Los media    popular
# 66 a 75    bastante fácil    novela, revista femenina    12 años
# 76 a 85    fácil    para quioscos    11 años
# 86 a 100    muy fácil    cómics, tebeos y viñetas    6 a 10 años

import os
from syllabic import Tokenizer
from syllabicator import Silabicador


class TextClassifier(Tokenizer):
    
    def __init__(self, corpus_dir):
        self.by_readability = [[] for i in range(7)]
        self.syllabicator = Silabicador()
        for root, dirs, files in os.walk(corpus_dir):
            for file in files:
                file_path = root + file
                with open(file_path, "r") as f:
                    content = f.read()
                readability = self.readability(content)
                pair = (readability, file_path)
                if 0 <= readability <= 15:
                    self.by_readability[0].append(pair)
                elif 16 <= readability <= 35:
                    self.by_readability[1].append(pair) 
                elif 36 <= readability <= 50:
                    self.by_readability[2].append(pair)
                elif 51 <= readability <= 65:
                    self.by_readability[3].append(pair)
                elif 66 <= readability <= 75:
                    self.by_readability[4].append(pair)
                elif 76 <= readability <= 85:
                    self.by_readability[5].append(pair)
                elif 86 <= readability:
                    self.by_readability[6].append(pair)

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
            S += len(self.syllabicator(token))
            
        P = len(tokens)
        F = len(sentences)
        return 206.835 - (62.3 * (S/P)) - (P/F)