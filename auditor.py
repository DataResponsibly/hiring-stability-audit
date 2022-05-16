from statistics_helpers import *
from visualization_helpers import *
from ADS import *

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import functools
from functools import partial

class Auditor():
    """ To evaluate the stability of the ADS on different metrics"""
    """ 
    Input:
        score_names: list of column names that contain scores/labels
        primary_key: to identify records across treatment and control and demographic information
        control: dataframe with scores from control group
        treatment: dictionary of treatment name and treatment scores dataframe
        groups_of_interest: dictionary of column name (gender, race, etc) and value corresponding to group(s) of interest.
                            all other rows are treated as "other".
        demographics: dataframe with demographic information such as gender, race, age, etc
        """
    
    def __init__(self, score_names, primary_key, control, treatment, demographics, groups_of_interest):
        self.score_names = score_names
        self.ID = primary_key
        self.control = control
        self.treatment = treatment
        self.groups_of_interest = groups_of_interest
        self.index_by_group = get_index_by_group(demographics, groups_of_interest)

        
    def compute_total_variation(self, measure=L1_distance):
        """
        currently only computes L1_norm, but you can plug in any other distance measure, such as spatial distances from scipy
        """
        total_variation = pd.DataFrame({})
        
        for treatment_name in self.treatment.keys():
            # Broken out by subgroups:
            for i in self.index_by_group:
                for j in self.index_by_group[i]:
                    control = self.control.loc[self.index_by_group[i][j]][self.score_names]
                    treatment = self.treatment[treatment_name].loc[self.index_by_group[i][j]][self.score_names]
            
                    tv = measure(control, treatment)
                    tv_df = pd.DataFrame({}).append([tv.mean(),tv.std()], ignore_index=True)
                    tv_df.index=[[treatment_name, treatment_name], [str(i+"_"+j), str(i+"_"+j)], ["mean", "std"]]
                    total_variation = total_variation.append(tv_df)

        return total_variation
        
    def compute_statistic(self, test=wilcoxon):
        """
        Possible correlation tests: "spearman", "pearsons", "kendall_tau"

        Possible hypothesis tests:
            Parametric tests: "student_t", "paired_student_t", "anova"
            Non-parametric tests: "mann_whitney_u", "wilcoxon", "kruskal_wallis_h"

        default: "wilcoxon"
        User can also plug in any custom function for correlation testing, such as other scipy implementations
        """
        statistic_df = pd.DataFrame({})
        
        for treatment_name in self.treatment.keys():
            # Broken out by subgroups:
            for i in self.index_by_group:
                for j in self.index_by_group[i]:
                    control = self.control.loc[self.index_by_group[i][j]][self.score_names]
                    treatment = self.treatment[treatment_name].loc[self.index_by_group[i][j]][self.score_names]
                    
                    statistic_df = statistic_df.append(pd.DataFrame(test(control, treatment),
                             index=[[treatment_name, treatment_name], [str(i+"_"+j), str(i+"_"+j)],["correlation", "p_value"]]))

        return statistic_df
        
    def visualize_scores(self, axislim=None):
        num_treatments = len(self.treatment.keys())
        num_scores = len(self.score_names)

        number_of_columns = num_scores
        number_of_rows = num_treatments

        plt.figure(figsize=(20, 20), facecolor='white', dpi=300)
        plt.rc('font', family='Times New Roman')

        # Add space between subplots
        plt.subplots_adjust(hspace=0.33)
        plt.subplots_adjust(wspace=0.33)

        position = range(1,number_of_columns*number_of_rows + 1)
        fig = plt.figure(1)

        k=0
        for t in range(len(self.treatment.keys())):
            treatment_name = [*self.treatment][t]

            for s in range(len(self.score_names)):
                score_name = [*self.score_names][s]

                ax = fig.add_subplot(number_of_rows,number_of_columns,position[k])

                ax.plot(np.linspace(-0.1, 100.1, 10), np.linspace(-0.1, 100.1, 10), 
                     color = 'red', alpha=0.5, label='Y=X')

                ax.scatter(x=self.control[score_name], y=self.treatment[treatment_name][score_name], 
                       color='green', s=8, alpha=0.75, label=str(len(self.treatment[treatment_name][score_name]))+' participants')

                if axislim!=None:
                    ax.set_xlim(0, axislim)
                    ax.set_ylim(0, axislim)
                    
                ax.set_title(score_name, fontsize=12)
                ax.set_xlabel("control", fontsize=12)
                ax.set_ylabel("treatment: "+treatment_name, fontsize=12)
                ax.legend(frameon = True, fontsize=12, framealpha = 0.75, markerscale=3)

                k+=1

        plt.show()
        

    def visualize_total_variation(self):
        for treatment_name in self.treatment:
            visualize_tv(self, treatment_name)
            print(" \n \n \n")
        
    
    def multiple_hypothesis_correction(self, pvals, alpha = 0.05, method='bonferroni'):
        df = correct_pvalues(self, pvals, alpha, correction=method)
        return df

    
""" Helper functions """

def get_index_by_group(demographic_df, groups_of_interest):
    group_index = {"overall": {"_":demographic_df.index.values}}
    
    if len(groups_of_interest) == 0:
        return group_index
    
    for group_type in [*groups_of_interest]:
        temp={}
        for group in groups_of_interest[group_type]:
            temp[group] = demographic_df.loc[demographic_df[group_type] == group].index.values

        # "others" is just all other rows:
        temp["others"] = demographic_df[~demographic_df[group_type].isin(groups_of_interest[group_type])].index.values

        group_index[group_type] = temp
    
    return group_index
        