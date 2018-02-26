# -*- coding:utf-8 -*-

import os
import sys
from syllabic import SyllableStatistics

if len(sys.argv) < 2: 
    raise Exception("Usage: python %s PATH_CORPUS_FOLDER" % sys.argv[0].split("/")[-1])

if not os.path.exists(sys.argv[1]):
    raise OSError("The provided path does not exist")
elif not os.path.isdir(sys.argv[1]):
    raise TypeError("PATH_CORPUS_FOLDER must be a folder")

stats = SyllableStatistics(sys.argv[1])
