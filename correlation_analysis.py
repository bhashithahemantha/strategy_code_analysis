import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from data_store_retrieve import DatabaseModel


# retrieve data from db - conf = 'ES_DAILY' or ....
def retrieve_data(conf):
    retrieved_data = DatabaseModel (conf).find_all ({})

    # creating a data frame from retrieved data
    data_frame = pd.DataFrame(data=retrieved_data)

    # creating a list from the data frame
    attribute_list = list(data_frame.keys())

    # creating a list of attributes to be removed
    exclude_list = ['_id']

    # remove unnessasury attributes - needs to be converted sets
    attribute_list = set(attribute_list).symmetric_difference(set(exclude_list))
    print(attribute_list.__len__())
    # final result
    final_data_set = data_frame.loc[:, attribute_list]
    # with pd.option_context ('display.max_rows', None, 'display.max_columns', None):
    #     print(final_data_set)
    return final_data_set


# scale the final data set
def scale_data(data_set):
    scaler_obj = MinMaxScaler()
    scaled_data_set = scaler_obj.fit_transform(data_set)
    print(scaled_data_set)
    return scaled_data_set


# check correlation and plot simple graph
def correlation_plot(data_set):
    # Get current size
    fig_size = plt.rcParams[ "figure.figsize" ]
    fig_size[ 0 ] = 100
    fig_size[ 1 ] = 100
    plt.rcParams[ "figure.figsize" ] = fig_size
    plt.matshow(data_set.corr())
    plt.xticks (range (len (data_set.columns)), data_set.columns);
    plt.yticks (range (len (data_set.columns)), data_set.columns);
    plt.title('ES_DAILY')
    plt.show()


# plot the correlation plot
data = retrieve_data("ES_DAILY")
correlation_plot(data)
# data_set = data.describe()
# correlation_matrix = np.corrcoef(data.T)
# with pd.option_context ('display.max_rows', None, 'display.max_columns', None):
    # print (correlation_matrix)

