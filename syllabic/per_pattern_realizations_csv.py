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
    raise Exception("Usage: python %s PATH_CORPUSES_FOLDER" % sys.argv[0].split("/")[-1])

if not os.path.exists(sys.argv[1]):
    raise OSError("The provided path does not exist")
elif not os.path.isdir(sys.argv[1]):
    raise TypeError("PATH_CORPUSES_FOLDER must be a folder")

corpora = ["Ceele", "cuentos", "excale"]
columns = ["%s_%d" % (corpus, level) for corpus in corpora for level in range(1,8)]
columns += ["Pattern"]
columns += ["Total"]

syllable_df = pd.DataFrame(columns=columns)
word_df = pd.DataFrame(columns=columns)

corpuses_path = sys.argv[1]
if corpuses_path.endswith("/"):
    corpuses_path = corpuses_path[:-1]

for corpus in os.listdir(corpuses_path):
    corpus_path = corpuses_path + "/%s" % corpus
    if not os.path.isdir(corpus_path):
        continue
    for level in os.listdir(corpus_path):
        try:
            int(level)
        except:
            continue

        level_path = corpus_path + "/%s" % level
        print("Procesing corpus %s level %s" % (corpus, level))
        stats = SyllableStatistics(level_path)

        level = int(level)
        for syllable, freq in stats.syllable_freqs.items():
            if syllable not in syllable_df.index:
                syllable_df.loc[syllable] = [0 for _ in range(len(columns))]
            syllable_df["%s_%d" % (corpus, level)][syllable] = freq
            syllable_df["Pattern"][syllable] = stats.pattern_index[syllable]

        for word, freq in stats.word_freqs.items():
            if word not in word_df.index:
                word_df.loc[word] = [0 for _ in range(len(columns))]
            word_df["%s_%d" % (corpus, level)][word] = freq
            word_df["Pattern"][word] = stats.wordpattern_index[word]

for sylpattern in syllable_df["Pattern"]:
    temp_df = syllable_df.loc[syllable_df['Pattern'] == sylpattern]
    temp_df = temp_df.drop("Pattern", 1)
    temp_df["Total"] = temp_df.sum(axis=1)
    temp_df = temp_df.sort_values("Total", ascending=False)
    temp_df.loc["Total"] = pd.Series(temp_df.sum())
    temp_df.transpose().to_csv(results_folder + \
                               "sylpatterns/%s.csv" % sylpattern) 
    
    # Normalized globally
    (temp_df / temp_df["Total"][-1]).transpose().to_csv(results_folder + \
                                    "sylpatterns/globally_normalized_%s.csv" % \
                                                               sylpattern)
    # Normalize individually
    normalize_for_individual_corpus(temp_df).transpose().to_csv(results_folder + \
                                    "sylpatterns/locally_normalized_%s.csv" % \
                                                               sylpattern)

for wordpattern in word_df["Pattern"]:
    temp_df = word_df.loc[word_df['Pattern'] == wordpattern]
    temp_df = temp_df.drop("Pattern", 1)
    temp_df["Total"] = temp_df.sum(axis=1)
    temp_df = temp_df.sort_values("Total", ascending=False)
    temp_df.loc["Total"] = pd.Series(temp_df.sum())
    temp_df.transpose().to_csv(results_folder + \
                               "wordpatterns/%s.csv" % wordpattern) 
    
    # Normalized globally
    (temp_df / temp_df["Total"][-1]).transpose().to_csv(results_folder + \
                                    "wordpatterns/globally_normalized_%s.csv" % \
                                                               wordpattern)
    # Normalize individually
    normalize_for_individual_corpus(temp_df).transpose().to_csv(results_folder + \
                                    "wordpatterns/locally_normalized_%s.csv" % \
                                                               wordpattern)
