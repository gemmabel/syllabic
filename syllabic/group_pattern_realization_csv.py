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
    rows = {}
    for level in os.listdir(corpus_path):
        try:
            int(level)
        except:
            continue
        level_path = corpus_path + "/%s" % level
        if os.path.isdir(level_path):
            print("Procesing corpus %s level %s" % (corpus, level))
            stats = SyllableStatistics(level_path)

            for pattern in stats.patterns:
                # Ensure column dict
                rows[pattern] = rows.get(pattern, {})
                for syllable in stats.syllable_index[pattern]:
                    # Ensure zero
                    rows[pattern][syllable] = rows[pattern].get(syllable, 0)
                    rows[pattern][syllable] += stats.syllable_freqs[syllable]
    corpus_dataframe = pd.DataFrame.from_dict(rows).fillna(0)
    corpus_dataframe = corpus_dataframe.transpose()
    corpus_dataframe.to_csv(corpus_path + "/%s_all_results.csv" % corpus)
