import re


def remove_values_from_list(the_list, val1):
    while val1 in the_list:
        the_list.remove(val1)
    return the_list


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


