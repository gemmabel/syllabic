import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind, kendalltau

inputfiles = ["../results/syllable.csv",
              "../results/sylpattern.csv",
              "../results/word.csv",
              "../results/wordpattern.csv"
             ]

for path in inputfiles:
    df = pd.read_csv(path, index_col=0)
    obs = df.iloc[:-1, :-1]

    kendall_table = pd.DataFrame(columns=obs.columns)
    p_table = pd.DataFrame(columns=obs.columns)
    for comparee in obs.columns:
        kendall_table.loc[comparee] = [1. for n in range(len(obs.columns))]
        p_table.loc[comparee] = [0. for n in range(len(obs.columns))]
        for comparator in obs.columns:
            if comparator != comparee:
                x = obs[comparator].rank(ascending=False)
                y = obs[comparee].rank(ascending=False)
                k_tau = kendalltau(x,y)
                kendall_table[comparator][comparee] = k_tau.correlation
                p_table[comparator][comparee] = k_tau.pvalue
    import ipdb;ipdb.set_trace()
    per = df.iloc[:-1,:-1]
    for i in range(len(per.columns)):
        per.iloc[:,i] = per.iloc[:,i] / df.iloc[:,i]['Total']*100
    chi2, p_chi2, dof, expected = chi2_contingency(obs.as_matrix(), correction=False)
    chi2_t, p_chi2_t, dof_t, expected_t = chi2_contingency(
                                                obs.transpose().as_matrix(),
                                                correction=False)
    import ipdb;ipdb.set_trace()
