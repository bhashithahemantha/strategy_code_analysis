import re
from data_store_retrieve import DatabaseModel

base = '/Users/bhashi/Desktop/ES_Daily_Data'
strategy_input = '{ Strategy inputs }\n'
ve_for_blank_line = "\n"
no_of_strategies = input('No of Strategies: ')
str_data = []


# def to check availability
def check_availability(key_1, value_1):
    if file_1.find (key_1) != -1:
        data[ value_1 ] = 1
    else:
        data[ value_1 ] = 0


for str_num in (range(1, int(no_of_strategies)+1)):
    file_1 = open (base + '/' + str (str_num) + '/Strategy Code.txt').read ()
    file = open (base + '/' + str (str_num) + '/Strategy Code.txt')

    data = {}
    Inputs = []
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

    check_availability (' stop;', 'breakout')
    check_availability ('MaxList', 'max_list')
    check_availability ('MinList', 'min_list')
    check_availability ('Average', 'average')
    check_availability ('XAverage', 'x_average')
    check_availability ('Momentum', 'momentum')
    check_availability ('NBarEn1', 'time_exit')
    check_availability ('RSI', 'rsi')
    check_availability ('TRIX', 'trix')
    check_availability ('ZLTrend', 'zero_lag_trend')
    check_availability ('AvgTrueRange', 'avg_true_range')
    check_availability ('MACD', 'macd')
    check_availability ('DMIPlus', 'dmi_plus')
    check_availability ('DMIMinus', 'dmi_minus')
    check_availability ('Highest', 'highest')
    check_availability ('Lowest', 'lowest')
    check_availability ('CCI', 'cci')


    # print(data)
    str_data.append(data)

# print(str_data)
print(str_data.__len__())

# DatabaseModel("ES_DAILY").insert(str_data)