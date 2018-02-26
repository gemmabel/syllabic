# -*- coding: utf-8 -*-

import re
import os
import string
from syllabicator import Silabicador
from unidecode import unidecode
from collections import OrderedDict,Counter
import numpy as np


class Tokenizer(object):

    def unique_chars(self, text):
        chars = set(list(text))
        return chars

    def remove_punctuation(self, text):
        text = text.replace('\n','')
        return re.sub(u'[^a-zA-Z]', '', unidecode(text))

    def tokenize(self, text):
        tokens = []
        for token in text.split(" "):
            if token != "":
                tokens.append(self.remove_punctuation(token).lower())
        return tokens


class SyllableStatistics(Tokenizer):

    def __init__(self, corpus_path, with_accents=False):

        self.syllables = set()
        self.patterns = set()

        self.pattern_freqs = {}
        self.syllable_freqs = {}

        self.syllable_probabilities = {}
        self.pattern_probabilities = {}

        silabicador = Silabicador()
        total_syllables = 0

        for filepath in os.listdir(corpus_path):
            if not os.path.isdir(corpus_path + "/" +  filepath):
                with open(corpus_path + "/" + filepath, "r", encoding="utf8") as f:
                    content = f.read()
                tokens = self.tokenize(content)
                for token in tokens:
                    syllables, patterns = silabicador(token)
                    total_syllables += len(syllables)
                    self.syllables = self.syllables.union(syllables)
                    self.patterns = self.patterns.union(patterns)
                    for syllable in syllables:
                        self.syllable_freqs[syllable] = 1 + \
                                self.syllable_freqs.get(syllable, 0)
                    for pattern in patterns:
                        self.pattern_freqs[pattern] = 1 + \
                                self.pattern_freqs.get(pattern, 0)

        # Calculate probabilities
        for syllable, freq in self.syllable_freqs.items():
            self.syllable_probabilities[syllable] = freq / total_syllables

        for pattern, freq in self.pattern_freqs.items():
            self.pattern_probabilities[pattern] = freq / total_syllables

        self.pattern_probabilities = np.array(sorted(
                                            self.pattern_probabilities.items()
                                                    )
                                            )
        self.syllable_probabilities = np.array(sorted(
                                            self.syllable_probabilities.items()
                                                    )
                                            )
