# -*- coding: utf-8 -*-

import re
import os
import string
from syllabicator import Silabicador
from unidecode import unidecode
from collections import OrderedDict,Counter
import numpy as np

import nltk.data

import codecs


class Tokenizer(object):

    def __init__(self, nltk_tokenizer="tokenizers/punkt/spanish.pickle"):
        self.sentence_tokenizer = nltk.data.load(nltk_tokenizer)

    def unique_chars(self, text):
        chars = set(list(text))
        return chars

    def remove_punctuation(self, text):
        text = text.replace('\n','')
        return re.sub(u'[^a-zA-Z]', '', unidecode(text))

    def normalize(self, text):
        temp_text = re.sub(r'[^\w\s]',
                           '',
                           text,
                           re.UNICODE).replace("\t",
                                               "").replace("\n",
                                                           "").lower()
        temp_text = self.remove_punctuation(temp_text)
        return temp_text

    def tokenize(self, text):
        tokens = []
        for token in text.split(" "):
            token = self.normalize(token)
            if token != "":
                tokens.append(token)
        return tokens

    def sentences(self, text):
        return self.sentence_tokenizer.tokenize(text)


class SyllableStatistics(Tokenizer):

    def __init__(self, corpus_path, with_accents=False):
        super(SyllableStatistics, self).__init__()

        self.syllables = set()
        self.patterns = set()
        self.words = set()
        self.wordpatterns = set()

        self.pattern_freqs = {}
        self.syllable_freqs = {}
        self.word_freqs = {}
        self.wordpattern_freqs = {}

        self.syllable_probabilities = {}
        self.pattern_probabilities = {}
        self.word_probabilities = {}
        self.wordpattern_probabilities = {}

        self.total_syllables = 0

        self.pattern_index = {}

        silabicador = Silabicador()

        for filepath in os.listdir(corpus_path):
            if not os.path.isdir(corpus_path + "/" +  filepath):
                try:
                    with open(corpus_path + "/" + filepath, "r",
                              encoding="utf-8") as f:
                        content = f.read()
                except:
                    with codecs.open(corpus_path + "/" + filepath,
                                     "r", "latin-1") as f:
                        content = f.read()
                    with codecs.open(corpus_path + "/" + filepath, 
                                     "w", "utf-8") as f:
                        f.write(content)
                    with open(corpus_path + "/" + filepath, "r",
                              encoding="utf-8") as f:
                        content = f.read()

                tokens = self.tokenize(content)
                for token in tokens:
                    syllables, patterns = silabicador(token)
                    self.total_syllables += len(syllables)
                    self.syllables = self.syllables.union(syllables)
                    self.patterns = self.patterns.union(patterns)

                    # Register syllables and patterns
                    for i in range(len(syllables)):
                        syllable = syllables[i]
                        pattern = patterns[i]
                        if syllable not in self.pattern_index.keys():
                            self.pattern_index[syllable] = pattern
                        self.syllable_freqs[syllable] = 1 + \
                                self.syllable_freqs.get(syllable, 0)
                        self.pattern_freqs[pattern] = 1 + \
                                self.pattern_freqs.get(pattern, 0)

                    # Register words and wordpatterns
                    word = token
                    wordpattern = "".join(patterns)
                    self.word_freqs[word] = 1 + \
                            self.word_freqs.get(word, 0)
                    self.wordpattern_freqs[wordpattern] = 1 + \
                            self.wordpattern_freqs.get(wordpattern, 0)

        # Calculate probabilities
        for syllable, freq in self.syllable_freqs.items():
            self.syllable_probabilities[syllable] = freq / self.total_syllables

        for pattern, freq in self.pattern_freqs.items():
            self.pattern_probabilities[pattern] = freq / self.total_syllables

        for word, freq in self.word_freqs.items():
            self.word_probabilities[word] = freq / len(tokens)

        for wordpattern, freq in self.wordpattern_freqs.items():
            self.wordpattern_probabilities[wordpattern] = freq / len(tokens)

    def to_row(self, syllable):
        row = {}
        # columns = ["Level", "Syllable", "SyllableFrequency", "Pattern",
        # "PatternFrequency", "SyllableProbability", "PatternProbability",
        # "TotalSyllables"]
        if syllable in self.syllables:
            row["Syllable"] = syllable
            row["SyllableFrequency"] = self.syllable_freqs[syllable]
            row["Pattern"] = self.pattern_index[syllable]
            row["PatternFrequency"] = self.pattern_freqs[row["Pattern"]]
            row["SyllableProbability"] = self.syllable_probabilities[syllable]
            row["PatternProbability"] = self.pattern_probabilities[row["Pattern"]]
            row["TotalSyllables"] = self.total_syllables
        return row
