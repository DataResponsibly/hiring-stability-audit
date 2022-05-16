import numpy as np
import matplotlib.pyplot as plt
from statistics_helpers import *
import pandas as pd

def visualize_tv(self, treatment_name):
    for group_type in self.index_by_group:
        
        if group_type == 'overall':
            #No subplots
            control = self.control.loc[self.index_by_group['overall']['_']][self.score_names]
            treatment = self.treatment[treatment_name].loc[self.index_by_group['overall']['_']][self.score_names]

            tv = L1_distance(control, treatment)
            
            plt.figure(figsize=(16,4))
            ax = plt.subplot(111)
            ax.boxplot(tv, labels = self.score_names)
            ax.set_title("Treatment: "+treatment_name, fontsize=22)
            ax.grid(which='both', axis='y', alpha=0.3)
            ax.set_ylabel(group_type, fontsize=30)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            ax.tick_params(left=False, bottom=False)
            ax.grid(which='both', axis='y', alpha=0.3)
            ax.set_axisbelow(True)
            plt.show()
        
        else:
            fig, ax = plt.subplots(1, len(self.index_by_group[group_type]),figsize=(16,4), sharey=True)

            for g, group_name in enumerate(self.index_by_group[group_type]):
                control = self.control.loc[self.index_by_group[group_type][group_name]][self.score_names]
                treatment = self.treatment[treatment_name].loc[self.index_by_group[group_type][group_name]][self.score_names]

                tv = L1_distance(control, treatment)

                if g==0:
                    ax[g].set_ylabel(group_type, fontsize=30)


                ax[g].boxplot(tv, labels = self.score_names)
                ax[g].set_title(group_name, fontsize=22)

                ax[g].spines['right'].set_visible(False)
                ax[g].spines['top'].set_visible(False)

                ax[g].tick_params(left=False, bottom=False)
                ax[g].grid(which='both', axis='y', alpha=0.3)
                ax[g].set_axisbelow(True)

                if g!=0:
                    ax[g].spines['left'].set_visible(False)

            plt.subplots_adjust(hspace=0.4)
        plt.show()