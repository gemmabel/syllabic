import pandas as pd
from scipy.stats import chi2_contingency, chisquare, ttest_ind

inputfiles = ["../results/syllable.csv",
              "../results/sylpattern.csv",
              "../results/word.csv",
              "../results/wordpattern.csv"
             ]
for path in inputfiles:
    df = pd.read_csv(path, index_col=0)
    obs = df.iloc[:-1, :-1]
    ttest_df = pd.DataFrame(columns=obs.columns)
    for row in obs.columns:
        for column in obs.columns:
            ttest_ind()
            ttest_df[column].loc[row] = 
    chi2, p_chi2, dof, expected = chi2_contingency(obs)
    chisq, p_chisq = chisquare(obs, expected)
    import ipdb;ipdb.set_trace()
