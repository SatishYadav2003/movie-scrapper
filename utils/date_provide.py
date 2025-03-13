import datetime


def date_provide():

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
    return formatted_datetime