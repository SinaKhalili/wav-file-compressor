"""
LZW compression - dictionary creation on-the-fly
"""


def get_message(message):
    """
    Returns the message as an array of integers
    """

    dictionary = {}
    dict_counter = 0
    output = []
    p = ""

    for c in message:
        combined_string = str(p) + str(c)
        if combined_string in dictionary:
            p = str(combined_string)
        else:
            if str(p) not in dictionary:
                dictionary[str(p)] = dict_counter
                dict_counter += 1

            output.append(dictionary[str(p)])
            dictionary[combined_string] = dict_counter
            dict_counter += 1
            p = str(c)

    return output
