import datetime


def values_from_list_of_dictionaries(list_of_dictionaries, key):
    return [item[key] for item in list_of_dictionaries]


def add_0_before_numbers_under_10_convert_to_datetime(format_list, dictionary):
    date_str = ""
    for key in format_list:
        if int(dictionary[key]) < 10:
            dictionary[key] = "0{}".format(dictionary[key])
        date_str += dictionary[key]

    return datetime.datetime.strptime(date_str, "%Y%m%d%H%M")