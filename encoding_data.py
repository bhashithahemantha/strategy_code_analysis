# data is dataframe
def data_encoding(data):
    data_objects_cp = data.select_dtypes(include=['object']).copy()

    for key in data_objects_cp.keys():
        data_objects_cp[key] = data_objects_cp[key].astype('category')
        data_objects_cp[key] = data_objects_cp[key].cat.codes
        data[key] = data_objects_cp[key]
    encoded_data = data.fillna(0)
    return encoded_data



# # print(data_objects_cp)
    # # print (data_objects_cp.info ())
    # # converting object data types to categorical data types(only cat types can be encoded)
    # data_objects_cp['EntPrL'] = data_objects_cp['EntPrL'].astype('category')
    # data_objects_cp['EntPrS'] = data_objects_cp['EntPrS'].astype('category')
    # data_objects_cp['entry_act'] = data_objects_cp['entry_act'].astype('category')
    # data_objects_cp['entry_con'] = data_objects_cp['entry_con'].astype('category')
    # data_objects_cp['long_exit'] = data_objects_cp['long_exit'].astype('category')
    # data_objects_cp['short_exit'] = data_objects_cp['short_exit'].astype('category')
    # # print(data_objects_cp['short_exit'])
    # # print(type(data_objects_cp['short_exit']))
    # # generating cat code for the data types
    # data_objects_cp['EntPrL'] = data_objects_cp['EntPrL'].cat.codes
    # data_objects_cp['EntPrS'] = data_objects_cp['EntPrS'].cat.codes
    # data_objects_cp['entry_act'] = data_objects_cp['entry_act'].cat.codes
    # data_objects_cp['entry_con'] = data_objects_cp['entry_con'].cat.codes
    # data_objects_cp['long_exit'] = data_objects_cp['long_exit'].cat.codes
    # data_objects_cp['short_exit'] = data_objects_cp['short_exit'].cat.codes
    # # print ("code ", data_objects_cp[ 'short_exit' ])
    # # print (type (data_objects_cp[ 'short_exit' ]))
    # # printing the heads
    # # print(data_objects_cp.head())
    # # print (data_objects_cp.info ())
    #
    # # joining the encoded data with numarical data set
    # data['EntPrL'] = data_objects_cp['EntPrL']
    # data['EntPrS'] = data_objects_cp['EntPrS']
    # data['entry_act'] = data_objects_cp['entry_act']
    # data['entry_con'] = data_objects_cp['entry_con']
    # data['long_exit'] = data_objects_cp['long_exit']
    # data['short_exit'] = data_objects_cp['short_exit']
    # # printing the head to check NaN
    # # print(data.head())
    # # removing NaN
    #
    # encoded_data = data.fillna(0)
    # # remove correlations
    # # encoded_data = data.drop(['average', 'x_average', 'N1', 'trix', 'NBarEx1', 'highest', 'strategy_id'], axis=1)
    # return encoded_data

