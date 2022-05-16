import numpy as np
from scipy.spatial import distance
from scipy import stats 
import pandas as pd
from statsmodels.stats.multitest import multipletests

""" Correlation tests"""

def spearman(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.spearmanr(control[i], treatment[i])
    return correlation, pvalue

def pearsons(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.pearsonr(control[i], treatment[i])
    return correlation, pvalue

def kendall_tau(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.kendalltau(control[i], treatment[i])
    return correlation, pvalue


""" Parametric tests"""

def student_t(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.ttest_ind(control[i], treatment[i])
    return correlation, pvalue

def paired_student_t(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.ttest_rel(control[i], treatment[i])
    return correlation, pvalue

def anova(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.f_oneway(control[i], treatment[i])
    return correlation, pvalue


""" Non-Parametric tests"""

def mann_whitney_u(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.mannwhitneyu(control[i], treatment[i])
    return correlation, pvalue

def wilcoxon__(control, treatment):
    statistic = {}
    pvalue = {}
    
    #L1 = L1_distance(control, treatment)
    
    for i in control.columns:
        statistic[i], pvalue[i] = stats.wilcoxon(control[i], treatment[i])
            
    return statistic, pvalue

def wilcoxon(control, treatment):
    statistic = {}
    pvalue = {}
    
    L1 = L1_distance(control, treatment)
    
    for i in control.columns:       
        if(all(np.isclose(L1[i],0))):
            # Cannot perform Wilcoxon test if treatment and control are uniformly identical
            print("All differences are 0 for {}. Did not perform Wilcoxon signed rank test.".format(i))
            statistic[i] = np.nan
            pvalue[i] = np.nan

        else:
            # Two sided test Wilcoxon signed rank test
            # Look at paired differences between treatment and control
            # Test whether median difference is significantly different than zero
            statistic[i], pvalue[i] = stats.wilcoxon(control[i], treatment[i])
            
    return statistic, pvalue


def kruskal_wallis_h(control, treatment):
    correlation = {}
    pvalue = {}
    for i in control.columns:
        correlation[i], pvalue[i] = stats.kruskal(control[i], treatment[i])
    return correlation, pvalue


""" Measures of total variation """

def L1_distance(control, treatment):
    return np.abs(control-treatment)


""" Multiple hypothesis testing corrections """

def correct_pvalues(self, pvals, alpha, correction='bonferroni'):
    """ Uses the multipletests methods of statsmodels. Available correction methods are:
        'bonferroni' : one-step correction
        'sidak' : one-step correction
        'holm-sidak' : step down method using Sidak adjustments
        'holm' : step-down method using Bonferroni adjustments
        'simes-hochberg' : step-up method (independent)
        'hommel' : closed method based on Simes tests (non-negative)
        'fdr_bh' : Benjamini/Hochberg (non-negative)
        'fdr_by' : Benjamini/Yekutieli (negative)
        'fdr_tsbh' : two stage fdr correction (non-negative)
        'fdr_tsbky' : two stage fdr correction (non-negative)
    """
    pvals_nonnull = pvals.dropna()
    null_index = [i for i in pvals.index if i not in pvals_nonnull.index]
    reject, correct_p, __ , __ = multipletests(pvals_nonnull.values.flatten(), alpha, method=correction)
    corrected_pvals = pd.DataFrame(correct_p.reshape(pvals_nonnull.shape), columns = self.score_names, index=pvals_nonnull.index)
    temp = np.array([np.nan]*len(null_index)*len(self.score_names)).reshape(len(null_index), len(self.score_names))
    temp_df = pd.DataFrame(temp,columns = self.score_names, index=null_index)
    
    return corrected_pvals.append(temp_df)