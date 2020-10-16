import datetime


def switch(argument):
    switcher = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday",
        -1: "Complete",
    }
    return switcher.get(argument, "Invalid month")


print(switch(datetime.datetime.today().isoweekday()))
