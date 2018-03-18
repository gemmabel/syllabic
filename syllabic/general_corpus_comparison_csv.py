# -*- coding:utf-8 -*-

import os
import sys
import pandas as pd
from syllabic import SyllableStatistics

def normalize_for_individual_corpus(df, corpora=['Ceele', 'cuentos', 'excale']):
    all_total = 0
    past_total = df["Total"][-1]
    for corpus in corpora:
        corpus_total = df[corpus].loc['Total']
        all_total += corpus_total

        df[corpus] = df[corpus]/corpus_total
        df = df.drop("Total", 1)
        df["Total"] = df.sum(axis=1)
 
    if all_total != past_total:
        import ipdb;ipdb.set_trace()
        raise Exception("Incorrect total")
    return df

if len(sys.argv) < 2: 
    raise Exception("Usage: python %s PATH_CORPUS_FOLDER" % sys.argv[0].split("/")[-1])

if not os.path.exists(sys.argv[1]):
    raise OSError("The provided path does not exist")
elif not os.path.isdir(sys.argv[1]):
    raise TypeError("PATH_CORPUS_FOLDER must be a folder")

results_folder = "../results"

corpora = ["Ceele", "cuentos", "excale"]

syllable_dict = {}
word_dict = {}
wordpattern_dict = {}
sylpattern_dict = {}

for corpus in corpora:
    corpus_path = sys.argv[1] + "/" + corpus

    # Dataframe skeleton for corpus
    syllable_dict[corpus] = {}
    word_dict[corpus] = {}
    wordpattern_dict[corpus] = {}
    sylpattern_dict[corpus] = {}

    if not os.path.isdir(corpus_path):
        import ipdb;ipdb.set_trace()
        raise OSError("The corpus is not in the specified path")

    for level in os.listdir(corpus_path):
        try:
            int(level)
        except:
            continue

        print("Procesing corpus %s level %s" % (corpus, level))
        level_stats = SyllableStatistics(corpus_path + "/" + level)

        level = int(level)
        for syllable, freq in level_stats.syllable_freqs.items():
            syllable_dict[corpus][syllable] = \
                    syllable_dict[corpus].get(syllable, 0)
            syllable_dict[corpus][syllable] += freq

        for pattern, freq in level_stats.pattern_freqs.items():
            sylpattern_dict[corpus][pattern] = \
                    sylpattern_dict[corpus].get(pattern, 0)
            sylpattern_dict[corpus][pattern] += freq

        for word, freq in level_stats.word_freqs.items():
            word_dict[corpus][word] = \
                    word_dict[corpus].get(word, 0)
            word_dict[corpus][word] += freq

        for wordpattern, freq in level_stats.wordpattern_freqs.items():
            wordpattern_dict[corpus][wordpattern] = \
                    wordpattern_dict[corpus].get(wordpattern, 0)
            wordpattern_dict[corpus][wordpattern] += freq

# Convert to dataframe
syllable_df = pd.DataFrame.from_dict(syllable_dict).fillna(0)
word_df = pd.DataFrame.from_dict(word_dict).fillna(0)
wordpattern_df = pd.DataFrame.from_dict(wordpattern_dict).fillna(0)
sylpattern_df = pd.DataFrame.from_dict(sylpattern_dict).fillna(0)

syllable_df["Total"] = syllable_df.sum(axis=1)
syllable_df = syllable_df.sort_values("Total", ascending=False)
syllable_df.loc["Total"] = pd.Series(syllable_df.sum())
syllable_df.transpose().to_csv(results_folder + "/general_syllable.csv") 

# Normalized globally
(syllable_df / syllable_df["Total"][-1]).transpose().to_csv(results_folder + \
                                            "/globally_normalized_general_syllable.csv")
# Normalize individually
normalize_for_individual_corpus(syllable_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_general_syllable.csv")

word_df["Total"] = word_df.sum(axis=1)
word_df = word_df.sort_values("Total", ascending=False)
word_df.loc["Total"] = pd.Series(word_df.sum())
word_df.transpose().to_csv(results_folder + "/general_word.csv") 

# Normalized globally
(word_df / word_df["Total"][-1]).transpose().to_csv(results_folder + \
                                            "/globally_normalized_general_word.csv")

# Normalize individually
normalize_for_individual_corpus(word_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_general_word.csv")

wordpattern_df["Total"] = wordpattern_df.sum(axis=1)
wordpattern_df = wordpattern_df.sort_values("Total", ascending=False)
wordpattern_df.loc["Total"] = pd.Series(wordpattern_df.sum())
wordpattern_df.transpose().to_csv(results_folder + "/general_wordpattern.csv") 

# Normalized globally
(wordpattern_df / wordpattern_df["Total"][-1]).transpose().to_csv(results_folder + \
                                        "/globally_normalized_general_wordpattern.csv")

# Normalize individually
normalize_for_individual_corpus(wordpattern_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_general_wordpattern.csv")

sylpattern_df["Total"] = sylpattern_df.sum(axis=1)
sylpattern_df = sylpattern_df.sort_values("Total", ascending=False)
sylpattern_df.loc["Total"] = pd.Series(sylpattern_df.sum())
sylpattern_df.transpose().to_csv(results_folder + "/general_sylpattern.csv") 

# Normalized globally
(sylpattern_df / sylpattern_df["Total"][-1]).transpose().to_csv(results_folder + \
                                            "/globally_normalized_general_sylpattern.csv")

# Normalize individually
normalize_for_individual_corpus(sylpattern_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_general_sylpattern.csv")
