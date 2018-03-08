# -*- coding:utf-8 -*-

import os
import sys
import pandas as pd
from syllabic import SyllableStatistics

if len(sys.argv) < 2: 
    raise Exception("Usage: python %s PATH_CORPUS_FOLDER" % sys.argv[0].split("/")[-1])

if not os.path.exists(sys.argv[1]):
    raise OSError("The provided path does not exist")
elif not os.path.isdir(sys.argv[1]):
    raise TypeError("PATH_CORPUS_FOLDER must be a folder")

results_folder = "../results"

corpora = ["Ceele", "cuentos", "excale"]
columns = ["%s_%d" % (corpus, level) for corpus in corpora for level in range(1,8)]
columns += ["Total"]

syllable_df = pd.DataFrame(columns=columns)
word_df = pd.DataFrame(columns=columns)
wordpattern_df = pd.DataFrame(columns=columns)
sylpattern_df = pd.DataFrame(columns=columns)

for corpus in corpora:
    corpus_path = sys.argv[1] + "/" + corpus
    if not os.path.isdir(corpus_path):
        raise OSError("The corpus is not in the specified path")

    for level in os.listdir(corpus_path):
        try:
            int(level)
        except:
            continue
        level_stats = SyllableStatistics(corpus_path + "/" + level)

        level = int(level)
        for syllable, freq in level_stats.syllable_freqs.items():
            if syllable not in syllable_df.index:
                syllable_df.loc[syllable] = [0 for _ in range(len(columns))]
            syllable_df["%s_%d" % (corpus, level)][syllable] = freq

        for pattern, freq in level_stats.pattern_freqs.items():
            if pattern not in sylpattern_df.index:
                sylpattern_df.loc[pattern] = [0 for _ in range(len(columns))]
            sylpattern_df["%s_%d" % (corpus, level)][pattern] = freq

        for word, freq in level_stats.word_freqs.items():
            if word not in word_df.index:
                word_df.loc[word] = [0 for _ in range(len(columns))]
            word_df["%s_%d" % (corpus, level)][word] = freq

        for wordpattern, freq in level_stats.wordpattern_freqs.items():
            if wordpattern not in wordpattern_df.index:
                wordpattern_df.loc[wordpattern] = [0 for _ in range(len(columns))]
            wordpattern_df["%s_%d" % (corpus, level)][wordpattern] = freq

syllable_df["Total"] = syllable_df.sum(axis=1)
syllable_df.loc["Total"] = pd.Series(syllable_df.sum())
syllable_df.to_csv(results_folder + "/syllable.csv") 

word_df["Total"] = word_df.sum(axis=1)
word_df.loc["Total"] = pd.Series(word_df.sum())
word_df.to_csv(results_folder + "/word.csv") 

wordpattern_df["Total"] = wordpattern_df.sum(axis=1)
wordpattern_df.loc["Total"] = pd.Series(wordpattern_df.sum())
wordpattern_df.to_csv(results_folder + "/wordpattern.csv") 

sylpattern_df["Total"] = sylpattern_df.sum(axis=1)
sylpattern_df.loc["Total"] = pd.Series(sylpattern_df.sum())
sylpattern_df.to_csv(results_folder + "/sylpattern.csv") 
