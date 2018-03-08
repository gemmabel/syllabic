import pandas as pd

inputfiles = ["../results/syllable.csv",
              "../results/sylpattern.csv",
              "../results/word.csv",
              "../results/wordpattern.csv"
             ]
for path in inputfiles:
    df = pd.read_csv(path, index_col=0)
    import ipdb;ipdb.set_trace()
