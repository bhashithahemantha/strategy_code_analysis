import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from sklearn.preprocessing import StandardScaler

#
from data_store_retrieve import DatabaseModel
import encoding_data as ed

data_retrieved = DatabaseModel('CL_30').find_all({})

# drop _id from mongo
data = pd.DataFrame(data_retrieved).drop(['_id'], axis=1)

data = ed.data_encoding(data)

# -----------------------------------------------------------------------
# data normalization
def normalization(data):
    from sklearn import preprocessing
    # load the dataset
    print(data.shape)
    # separate the data from the target attributes
    X = data
    # normalize the data attributes
    normalized_data = preprocessing.normalize(X)
    # print(normalized_data)
    # plt.plot(normalized_data)
    # plt.show()
    return normalized_data
# print("nom_data_type", type(normalization(data)))
# print("nom_data", normalization(data))
# normalization(data)
# -----------------------------------------------------------------------
# data Standardization
def Standardization(data):
    from sklearn import preprocessing
    # load the dataset
    print(data.shape)
    # separate the data from the target attributes
    X = data
    # normalize the data attributes
    normalized_data = preprocessing.scale(X)
    print(normalized_data)
    plt.plot(normalized_data)
    plt.show()
# Standardization(data)
#-----------------------------------------------------------------------
def dagostinos_k_squared(data):
    k2, p = stats.normaltest(data)
    alpha = 1e-3
    print(len(p))
    if p.all() < alpha:  # null hypothesis: data comes from a normal distribution
        print("The null hypothesis can be rejected")
    else:
        print("The null hypothesis cannot be rejected")

# dagostinos_k_squared(data)
# # ------------------------------------------------------------------------
def histogram_plot(data):
    # histogram plot
    from matplotlib import pyplot
    # histogram plot
    pyplot.hist (data)
    pyplot.show ()
# histogram_plot(data)
# ------------------------------------------------------------------------
def QQ_plot(data):
    # QQ Plot
    from numpy.random import seed
    from numpy.random import randn
    from statsmodels.graphics.gofplots import qqplot
    from matplotlib import pyplot
    # q-q plot
    qqplot(data, line='s')
    pyplot.show ()
# QQ_plot(data)
# ------------------------------------------------------------------------
def shafiro_wilk(data):
    # Shapiro-Wilk Test
    from scipy.stats import shapiro
    # normality test
    stat, p = shapiro (data)
    print ('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print ('Sample looks Gaussian (fail to reject H0)')
    else:
        print ('Sample does not look Gaussian (reject H0)')
# shafiro_wilk(normalization(data))
# ------------------------------------------------------------------------
def anderson_darlin(data):
    # Anderson-Darling Test
    from scipy.stats import anderson
    # normality test
    for j in range(0, len(data)):
        result = anderson(data[j])
        print ('Statistic: %.3f' % result.statistic)
        p = 0
        for i in range (len (result.critical_values)):
            sl, cv = result.significance_level[ i ], result.critical_values[ i ]
            if result.statistic < result.critical_values[ i ]:
                print (j, '%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
            else:
                print (j, '%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))
# anderson_darlin(normalization(data))
# -----------------------------------------------------------------------
