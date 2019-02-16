import re
from data_store_retrieve import DatabaseModel
import get_condition_data as gcd
import encoding_data as ed
import progressbar
import pandas as pd
import csv
base = '/Users/bhashi/Desktop/CL_30_Data'
no_of_strategies = input('No of Strategies: ')
strategy_input = '{ Strategy inputs }\n'
entry_prices = '{ Entry prices }\n'
entry_and_exit_con = '{ Entry and exit conditions }\n'
ve_for_blank_line = "\n"
str_data = []



# def to check availability
def check_availability(file, data, key_1, value_1):
    if file.find (key_1) != -1:
        data[ value_1 ] = 1
    else:
        data[ value_1 ] = 0


# Strategy Code optimum
def get_data():
    bar = progressbar.ProgressBar(maxval=int(no_of_strategies)).start ()
    for str_num in (range(1, int(no_of_strategies)+1)):
        file_1 = open (base + '/' + str (str_num) + '/Strategy Code.txt').read ()
        file = open (base + '/' + str (str_num) + '/Strategy Code.txt')
        bar.update(str_num)

        data = {}
        Inputs = []
        prices = []
        entry_n_exit_con = []
        data["strategy_id"] = str_num
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
                line = file.__next__()
                while(1):
                    if line != ve_for_blank_line:
                        prices.append(line.rstrip('\n'))
                        line = file.__next__ ()
                    else:
                        break

            if line == entry_and_exit_con:
                line = file.__next__()
                while(1):
                    if line != ve_for_blank_line:
                        entry_n_exit_con.append(line.rstrip('\n'))
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
                details_array = re.split("\s\=\s",x)
                data[details_array[0]] = details_array[1].rstrip(';')
            except IndexError:
                continue

        # format entry and exit con to json
        for i in entry_n_exit_con:
            try:
                x = re.search ('.+\=.+', i).string
                details_array = re.split ("\s\=\s",x)
                data[details_array[0]] = details_array[1].rstrip (';')
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


        data_passed = gcd.get_condition_data(file_1)

        data['entry_con'] = data_passed[0]
        data['entry_act'] = data_passed[1]

        if len(data_passed[2]) != 0:
            data['long_exit'] = data_passed[2]
        if len(data_passed[3]) != 0:
            data['short_exit'] = data_passed[3]
        if len(data_passed[4]) != 0:
            data['normal_exit'] = data_passed[4]

        print(str_num, " ",  data)
        str_data.append(data)
    # print ('str_data_type ', type (str_data))
    # print(str_data)
    return str_data

final_data = get_data()
print(final_data)
DatabaseModel('CL_30').insert(final_data)

