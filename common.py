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


def remaining_time(lst):
    for i in lst:
        time_left = i['deadline'] - datetime.datetime.now()
        print("time_left", time_left)
        s = time_left.total_seconds()
        print("s", s)
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        if s < 0:
            i['time_left'] = "overdue"
        elif time_left.days > 0:
            if time_left.days == 1:
                i['time_left'] = "{} day left".format(time_left.days)
            else:
                i['time_left'] = "{} days left".format(time_left.days)
        elif hours > 0:
            if hours == 1:
                i['time_left'] = "{} hour left".format(int(hours))
            else:
                i['time_left'] = "{} hours left".format(int(hours))
        elif minutes > 0:
            if minutes == 1:
                i['time_left'] = "{} minute left".format(int(minutes))
            else:
                i['time_left'] = "{} minutes left".format(int(minutes))
        elif seconds > 0:
            if seconds == 1:
                i['time_left'] = "{} second left".format(int(second))
            else:
                i['time_left'] = "{} seconds left".format(int(seconds))

    return lst


def format_time(lst):
    for i in lst:
        i['creation_time'] = i['creation_time'].strftime('%Y  /  %b / %-d - %H:%M')
        i['deadline'] = i['deadline'].strftime('%Y  /  %b / %-d - %H:%M')

    return lst
