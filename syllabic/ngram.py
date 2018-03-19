# -*- coding:utf-8 -*-

import os
import sys
from nltk import ngrams
from syllabic import SyllableStatistics
import numpy as np
from collections import Counter
import pandas as pd

if len(sys.argv) < 2: 
    raise Exception("Usage: python %s PATH_CORPUS_FOLDER" % sys.argv[0].split("/")[-1])

if not os.path.exists(sys.argv[1]):
    raise OSError("The provided path does not exist")
elif not os.path.isdir(sys.argv[1]):
    raise TypeError("PATH_CORPUS_FOLDER must be a folder")

if sys.argv[1].endswith("/"):
    corpora_path = sys.argv[1][:-1]
else:
    corpora_path = sys.argv[1]

results_folder = "../results"

corpora = ["Ceele", "cuentos", "excale"]
columns = ["%s_%d" % (corpus, level) for corpus in corpora for level in range(1,8)]
columns += ["Total"]

syllable_probabilities = pd.DataFrame(columns=columns)

bigram_probabilities = {}
unigram_probabilities = {}
trigram_probabilities = {}
for corpus in os.listdir(corpora_path):
    corpus_path = corpora_path + "/%s" % corpus
    if not os.path.isdir(corpus_path):
        continue

    for level in os.listdir(corpus_path):
        try:
            int(level)
        except:
            continue
        level_path = corpus_path + "/%s" % level
        if not os.path.isdir(level_path):
            continue

        level = int(level)
        stats = SyllableStatistics(level_path)

        # Unigrams
        unigram_probabilities["%s_%d" % (corpus, level)] = {}
        level_unigrams = []
        for word, number in stats.word_freqs.items():
            for _ in range(number):
                letter_ngram = ngrams(list(word), 1)
                for ngram in letter_ngram:
                    level_unigrams.append(ngram)

        total_unigrams = len(level_unigrams)
        unigram_freqs = Counter(level_unigrams)
        for unigram, freq in unigram_freqs.items():
            unigram_probabilities["%s_%d" % (corpus, level)
                                 ]["".join(unigram)] = freq / total_unigrams

        # Bigrams
        bigram_probabilities["%s_%d" % (corpus, level)] = {}
        level_bigrams = []
        for word, number in stats.word_freqs.items():
            for _ in range(number):
                letter_ngram = ngrams(list(word), 2)
                for ngram in letter_ngram:
                    level_bigrams.append(ngram)

        total_bigrams = len(level_bigrams)
        bigram_freqs = Counter(level_bigrams)
        for bigram, freq in bigram_freqs.items():
            bigram_probabilities["%s_%d" % (corpus, level)
                                ]["".join(bigram)] = freq / total_bigrams

        # Trigrams
        trigram_probabilities["%s_%d" % (corpus, level)] = {}
        level_trigrams = []
        for word, number in stats.word_freqs.items():
            for _ in range(number):
                letter_ngram = ngrams(list(word), 3)
                for ngram in letter_ngram:
                    level_trigrams.append(ngram)

        total_trigrams = len(level_trigrams)
        trigram_freqs = Counter(level_trigrams)
        for trigram, freq in trigram_freqs.items():
            trigram_probabilities["%s_%d" % (corpus, level)
                                 ]["".join(trigram)] = freq / total_trigrams

        # for syllable, freq in stats.syllable_freqs.items():
        #     if syllable not in syllable_probabilities.index:
        #         syllable_probabilities.loc[syllable] = [0 for _ in \
        #                                                 range(len(columns))]
        #     syllable_ngram = ngrams(list(syllable), 2)
        #     probability = 1
        #     for ngram in syllable_ngram:
        #         probability *= bigram_probabilities["%s_%d" % (corpus, level)
        #                                            ]["".join(ngram)]
        #     if probability < 1:
        #         syllable_probabilities["%s_%d" % (corpus, level)
        #                               ][syllable] = probability

unigram_df = pd.DataFrame.from_dict(unigram_probabilities).fillna(0)
unigram_df.to_csv(results_folder + "/unigrams.csv")
bigram_df = pd.DataFrame.from_dict(bigram_probabilities).fillna(0)
bigram_df.to_csv(results_folder + "/bigrams.csv")
trigram_df = pd.DataFrame.from_dict(trigram_probabilities).fillna(0)
trigram_df.to_csv(results_folder + "/trigrams.csv")

