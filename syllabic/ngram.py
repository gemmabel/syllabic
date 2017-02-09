# -*- coding:utf-8 -*-

import os
from syllabic import Tokenizer
import numpy as np
from unidecode import unidecode


class BiGram(Tokenizer):
    
    def __init__(self, corpus_path, with_accents=False):
        bag_of_pairs = {}
        probabilities = {}
        total_pairs = 0.
        for root, _, files in os.walk(corpus_path):
            for filepath in files:
                with open(root + "/" + filepath, "r") as f:
                    content = f.read()
                    
                tokens = self.tokenize(content)
                for token in tokens:
                    by_char_token = list(token)
                    for i in range(len(by_char_token)-1):
                        pair = by_char_token[i] +  by_char_token[i+1]
                        if not with_accents:
                            pair = unidecode(pair)
                        bag_of_pairs[pair] = bag_of_pairs.get(pair, 0) + 1
                        total_pairs += 1.
        
        # Calculate probabilities
        for pair, freq in bag_of_pairs.items():
            probabilities[pair] = freq/total_pairs
            
        self.probabilities = np.array(sorted(probabilities.items()))
        self.pairs = np.array(self.probabilities[:,0])
        self.proba = np.array(self.probabilities[:,1], dtype=np.float64)
            
    def generate_samples(self, n):
        return np.random.choice(self.pairs,
                                n,
                                p=self.proba)