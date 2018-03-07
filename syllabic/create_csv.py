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

columns = ["Level", "Syllable", "SyllableFrequency", "Pattern",
           "PatternFrequency", "SyllableProbability", "PatternProbability",
           "TotalSyllables"]

folder_dataframe = pd.DataFrame(columns=columns)
for level in os.listdir(sys.argv[1]):
    try:
        int(level)
    except:
        continue
    if os.path.isdir(sys.argv[1] + "/" + level):
        stats = SyllableStatistics(sys.argv[1] + "/" + level)
        for syllable in stats.syllables:
            row = stats.to_row(syllable)
            row["Level"] = level
            folder_dataframe.loc[level + "_" + syllable] = pd.Series(row)
folder_dataframe.to_csv(sys.argv[1] + "/results.csv")
