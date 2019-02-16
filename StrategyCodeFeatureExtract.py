import re
import pickle
import pandas as pd
strategy_input = '{ Strategy inputs }\n'
entry_prices = '{ Entry prices }\n'
entry_and_exit_con = '{ Entry and exit conditions }\n'
ve_for_blank_line = "\n"
list_passed = []
# def to check availability
def check_availability(file, data, key_1, value_1):
    if file.find (key_1) != -1:
        data[ value_1 ] = 1
    else:
        data[ value_1 ] = 0


# remove value from list
def remove_values_from_list(the_list, val1):
    while val1 in the_list:
        the_list.remove(val1)
    return the_list


# get condition data
def get_condition_data(file_1):
    words = re.split ("\s+|(\(|\)|<|>|=|;)", file_1)

    entry_conditions = [ ]
    entry_actions = [ ]
    long_exit = [ ]
    short_exit = [ ]
    normal_exit = [ ]

    is_if = False
    is_begin = False

    entry_current_condition = None
    entry_current_action = None

    entry_start = 0
    entry_end = 0

    end_array = [ ]

    # working
    for token in words:
        for i, j in enumerate (words):
            # take the start and end points for condition data
            if j == 'Entry':
                if words[ i + 2 ] == "orders":
                    entry_start = i
            if j == "Exit":
                if words[ i + 4 ] == "long":
                    entry_end = i
                    break
                if words[ i + 4 ] == "short":
                    entry_end = i
                    break
                if words[ i + 4 ] == "}":
                    entry_end = i
                    break
        break

    entry_tokens = words[ entry_start: entry_end ]

    for token in entry_tokens:
        # get condition data to an array
        if not token:
            continue
        elif token.lower () == "if":
            is_if = True
            entry_current_condition = [ ]
        elif token.lower () == "then":
            is_if = False
            entry_conditions.append (entry_current_condition)
        elif is_if:
            if token.isdecimal ():  # Detect numbers
                try:
                    entry_current_condition.append (int (token))
                except ValueError:
                    entry_current_condition.append (float (token))
            else:  # otherwise just take the string
                entry_current_condition.append (token)

        #         ------------------------------------------------

        elif token.lower () == "begin":
            is_begin = True
            entry_current_action = [ ]
        elif token.lower () == "end":
            is_begin = False
            entry_actions.append (entry_current_action)
        elif is_begin:
            if token.isdecimal ():  # Detect numbers
                try:
                    entry_current_action.append (int (token))
                except ValueError:
                    entry_current_action.append (float (token))
            else:  # otherwise just take the string
                entry_current_action.append (token)

    remove_values_from_list(entry_conditions, ';')
    remove_values_from_list(entry_actions[0], ';')
    remove_values_from_list(entry_actions[1], ';')

    # print (entry_conditions)
    # print (entry_actions)

    # working

    for i, e in reversed (list (enumerate (words))):
        if e == "end":
            end_array.append (i)
    # print(end_array)

    if "long" in words[ end_array[ 2 ]:end_array[ 1 ] ]:
        long_exit = words[ end_array[ 2 ] + 18:end_array[ 1 ] ]
        short_exit = words[ end_array[ 1 ] + 18:end_array[ 0 ] ]
        remove_values_from_list (long_exit, None)
        remove_values_from_list (long_exit, '')
        remove_values_from_list (long_exit, ';')

        remove_values_from_list (short_exit, None)
        remove_values_from_list (short_exit, '')
        remove_values_from_list (short_exit, ';')

        # print (long_exit)
        # print (short_exit)
    else:
        if "long" in words[ end_array[ 1 ]:end_array[ 0 ] ]:
            long_exit = words[ end_array[ 2 ]:end_array[ 1 ] ]
            remove_values_from_list (long_exit, None)
            remove_values_from_list (long_exit, ';')
            remove_values_from_list (long_exit, '')

            # print (long_exit)

        elif "short" in words[ end_array[ 1 ]:end_array[ 0 ] ]:
            short_exit = words[ end_array[ 1 ]:end_array[ 0 ] ]
            remove_values_from_list (short_exit, None)
            remove_values_from_list (short_exit, ';')
            remove_values_from_list (short_exit, '')

            # print (short_exit)

        else:
            normal_exit = words[ end_array[ 1 ]:end_array[ 0 ] ]
            remove_values_from_list (normal_exit, None)
            remove_values_from_list (normal_exit, '')
            remove_values_from_list (normal_exit, ';')

            # print (normal_exit)

    entry_conditions = ''.join(str(v) for v in entry_conditions[0]) + ''.join(str(v) for v in entry_conditions[1])
    entry_actions = ''.join(str(v) for v in entry_actions[0]) + ''.join(str(v) for v in entry_actions[1])
    long_exit = ''.join(str(v) for v in long_exit)
    short_exit = ''.join(str(v) for v in short_exit)
    normal_exit = ''.join(str(v) for v in normal_exit)
    # print(entry_conditions)
    # print(entry_actions)
    # print(long_exit)
    # print(short_exit)
    # print(normal_exit)
    return [entry_conditions,entry_actions,long_exit,short_exit,normal_exit]


# encoding object colomns
def data_encoding(data):
    data_objects_cp = data.select_dtypes (include=[ 'object' ]).copy ()

    for key in data_objects_cp.keys ():
        data_objects_cp[ key ] = data_objects_cp[ key ].astype ('category')
        data_objects_cp[ key ] = data_objects_cp[ key ].cat.codes
        data[ key ] = data_objects_cp[ key ]
    encoded_data = data.fillna (0)
    return encoded_data


# get strategy data
def get_data(file_path):
    file = open (file_path)
    file_1 = open (file_path).read()
    data = {}
    Inputs = [ ]
    prices = [ ]
    entry_n_exit_con = [ ]
    for line in file:
        # get inputs
        if line == strategy_input:
            line = file.__next__ ()
            while (1):
                if line != ve_for_blank_line:
                    # print(line)
                    Inputs.append (line.rstrip ("\n\t"))
                    # print(Inputs)
                    line = file.__next__ ()
                else:
                    break

        if line == entry_prices:
            line = file.__next__ ()
            while (1):
                if line != ve_for_blank_line:
                    prices.append (line.rstrip ('\n'))
                    line = file.__next__ ()
                else:
                    break

        if line == entry_and_exit_con:
            line = file.__next__ ()
            while (1):
                if line != ve_for_blank_line:
                    entry_n_exit_con.append (line.rstrip ('\n'))
                    line = file.__next__ ()
                else:
                    break

    # format inputs to the json
    Inputs[ 0 ] = "        " + (Inputs[ 0 ].split ('Inputs: ')[ 1 ])
    for i in Inputs:
        try:
            x = re.search ('\s+(\S+)\s\((\S+)\)?', i)
            if x:
                details_array = re.split ('\s', x.group (0))
                key = details_array[ 8 ]
                value = details_array[ 9 ].strip ('(')
                value = value.strip ('),')
                value = value.strip (');')
                if value == 'true':
                    value = 1
                elif value == 'false':
                    value = 0
                else:
                    value = float (value)
                data[ key ] = value
        except IndexError:
            continue

    # format prices to json
    for i in prices:
        try:
            x = re.search ('.+\=.+', i).string
            details_array = re.split ("\s\=\s", x)
            data[ details_array[ 0 ] ] = details_array[ 1 ].rstrip (';')
        except IndexError:
            continue

    # format entry and exit con to json
    for i in entry_n_exit_con:
        try:
            x = re.search ('.+\=.+', i).string
            details_array = re.split ("\s\=\s", x)
            data[ details_array[ 0 ] ] = details_array[ 1 ].rstrip (';')
        except IndexError:
            continue

    check_availability (file_1, data, ' stop;', 'breakout')
    check_availability (file_1, data, 'MaxList', 'max_list')
    check_availability (file_1, data, 'MinList', 'min_list')
    check_availability (file_1, data, 'Average', 'average')
    check_availability (file_1, data, 'XAverage', 'x_average')
    check_availability (file_1, data, 'Momentum', 'momentum')
    check_availability (file_1, data, 'NBarEn1', 'time_exit')
    check_availability (file_1, data, 'RSI', 'rsi')
    check_availability (file_1, data, 'TRIX', 'trix')
    check_availability (file_1, data, 'ZLTrend', 'zero_lag_trend')
    check_availability (file_1, data, 'AvgTrueRange', 'avg_true_range')
    check_availability (file_1, data, 'MACD', 'macd')
    check_availability (file_1, data, 'DMIPlus', 'dmi_plus')
    check_availability (file_1, data, 'DMIMinus', 'dmi_minus')
    check_availability (file_1, data, 'Highest', 'highest')
    check_availability (file_1, data, 'Lowest', 'lowest')
    check_availability (file_1, data, 'CCI', 'cci')

    data_passed = get_condition_data(file_1)

    data[ 'entry_con' ] = data_passed[ 0 ]
    data[ 'entry_act' ] = data_passed[ 1 ]

    if len (data_passed[ 2 ]) != 0:
        data[ 'long_exit' ] = data_passed[ 2 ]
    if len (data_passed[ 3 ]) != 0:
        data[ 'short_exit' ] = data_passed[ 3 ]
    if len (data_passed[ 4 ]) != 0:
        data[ 'normal_exit' ] = data_passed[ 4 ]

    return data

# load model
# some time later...
loaded_model = pickle.load (open ('/Users/bhashi/PycharmProjects/strategy_code_analysis/figures/k-means/trained_kmeans_model.sav', 'rb'))
data = get_data('/Users/bhashi/Downloads/CL30/Strategy Code.txt')
for key, value in data:
    temp = [key,value]
    list_passed.append(temp)
label = loaded_model.predict(list_passed[0])
print(type(label))
print(type(loaded_model))
print(label)