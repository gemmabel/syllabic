# -*- coding:utf-8 -*-

import os
import sys
import pandas as pd
from syllabic import SyllableStatistics

def normalize_for_individual_corpus(df, corpora=['Ceele', 'cuentos', 'excale']):
    all_total = 0
    past_total = df["Total"][-1]
    for corpus in corpora:
        columns = [ "%s_%d" % (corpus, level) for level in range(1, 8)]
        corpus_total = sum(df[columns].loc['Total'])
        all_total += corpus_total

        df[columns] = df[columns]/corpus_total
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

        print("Procesing corpus %s level %s" % (corpus, level))
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
syllable_df = syllable_df.sort_values("Total", ascending=False)
syllable_df.loc["Total"] = pd.Series(syllable_df.sum())
syllable_df.transpose().to_csv(results_folder + "/syllable.csv") 

# Normalized globally
(syllable_df / syllable_df["Total"][-1]).transpose().to_csv(results_folder + \
                                            "/globally_normalized_syllable.csv")
# Normalize individually
normalize_for_individual_corpus(syllable_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_syllable.csv")

word_df["Total"] = word_df.sum(axis=1)
word_df = word_df.sort_values("Total", ascending=False)
word_df.loc["Total"] = pd.Series(word_df.sum())
word_df.transpose().to_csv(results_folder + "/word.csv") 

# Normalized globally
(word_df / word_df["Total"][-1]).transpose().to_csv(results_folder + \
                                            "/globally_normalized_word.csv")

# Normalize individually
normalize_for_individual_corpus(word_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_word.csv")

wordpattern_df["Total"] = wordpattern_df.sum(axis=1)
wordpattern_df = wordpattern_df.sort_values("Total", ascending=False)
wordpattern_df.loc["Total"] = pd.Series(wordpattern_df.sum())
wordpattern_df.transpose().to_csv(results_folder + "/wordpattern.csv") 

# Normalized globally
(wordpattern_df / wordpattern_df["Total"][-1]).transpose().to_csv(results_folder + \
                                        "/globally_normalized_wordpattern.csv")

# Normalize individually
normalize_for_individual_corpus(wordpattern_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_wordpattern.csv")

sylpattern_df["Total"] = sylpattern_df.sum(axis=1)
sylpattern_df = sylpattern_df.sort_values("Total", ascending=False)
sylpattern_df.loc["Total"] = pd.Series(sylpattern_df.sum())
sylpattern_df.transpose().to_csv(results_folder + "/sylpattern.csv") 

# Normalized globally
(sylpattern_df / sylpattern_df["Total"][-1]).transpose().to_csv(results_folder + \
                                            "/globally_normalized_sylpattern.csv")

# Normalize individually
normalize_for_individual_corpus(sylpattern_df).transpose().to_csv(results_folder + \
                                            "/locally_normalized_sylpattern.csv")
