import re
# code = open("Strategy Code 1.txt").read()
# words = re.split("\s+|(\(|\)|<|>|=|;)", code)
# print(words)
base = '/Users/bhashi/Desktop/CL_Daily_Data'
no_of_strategies = input('No of Strategies: ')

for str_num in (range(1, int(no_of_strategies)+1)):
    file_1 = open (base + '/' + str (str_num) + '/Strategy Code.txt').read ()
    file = open (base + '/' + str (str_num) + '/Strategy Code.txt')
    words = re.split ("\s+|(\(|\)|<|>|=|;)", file_1)

    is_if = False

    entry_current_condition = None
    entry_current_action = None

    entry_conditions = []
    entry_actions = []

    entry_tokens = []
    act_tokens = []
    sell_act_tokens = []
    buy_act_tokens = []

    entry_start = 0
    entry_end = 0
    sell_act_start = 0
    buy_act_start = 0
    sell_act_end = 0
    buy_act_end = 0
    act_end = 0


    for token in words:
        for i, j in enumerate (words):
            # take the start and end points for condition data
            if j == 'Entry':
                if words[ i + 2 ] == "orders":
                    entry_start = i
            if j == "Exit":
                entry_end = i
        break

    entry_tokens = words[entry_start: entry_end]

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

    print (entry_conditions)






