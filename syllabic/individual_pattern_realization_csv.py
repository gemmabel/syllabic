# -*- coding:utf-8 -*-

import os
import sys
import pandas as pd
from syllabic import SyllableStatistics

if len(sys.argv) < 2: 
    raise Exception("Usage: python %s PATH_CORPUSES_FOLDER" % sys.argv[0].split("/")[-1])

if not os.path.exists(sys.argv[1]):
    raise OSError("The provided path does not exist")
elif not os.path.isdir(sys.argv[1]):
    raise TypeError("PATH_CORPUSES_FOLDER must be a folder")

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
        if os.path.isdir(level_path):
            print("Procesing corpus %s level %s" % (corpus, level))
            stats = SyllableStatistics(level_path)

            # Create dataframe
            columns = [pattern for pattern in stats.patterns]
            folder_dataframe = pd.DataFrame(columns=columns)
            for syllable in stats.syllables:
                row = {}
                row[stats.pattern_index[syllable]] = \
                                                stats.syllable_freqs[syllable]
                folder_dataframe.loc[syllable] = pd.Series(row)
            folder_dataframe = folder_dataframe.fillna(0)
            folder_dataframe = folder_dataframe.transpose()
            folder_dataframe.to_csv(corpus_path + "/%s_%s_results.csv" %
                                    (corpus,level))
