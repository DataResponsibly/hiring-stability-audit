import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import functools
from scipy.spatial import distance
from scipy import stats

class ADS():
    """ The personality prediction ADS """
    
    def __init__(self, score_names, primary_key):
        self.score_names = score_names
        self.ID = primary_key
    
    def score(self, X, score_func):
        """ return the personality scores for input resumes """
        return score_func(X=X, score_names=self.score_names, primary_key=self.ID)


# Helper functions: Different ways of obtaining scores
# User can plug in any custom score() function

def ADS_lookup(X, score_names, primary_key, filename):
        df = pd.read_csv(filename, index_col=primary_key)
        
        return df[score_names].loc[X]

def ADS_bullshitblackbox(X, score_names, primary_key, score_means, score_std):
    # Generate scores by sampling from a Gaussian with the same mean and std as the control scores
    df = pd.DataFrame({})
    
    for i in range(len(score_names)):   
        df[score_names[i]] = np.random.normal(score_means[i], 2*score_std[i], len(X))
    
    df[primary_key] = X
    df = df.set_index(primary_key)
    return df 