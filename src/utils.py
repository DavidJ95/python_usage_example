import datetime
import json
import re

def parse_date_txt(txt_search):
    """_summary_

    :param txt_search: Date entered as text. It may be in the form yyyy-mm-dd, refdate+nn, or today+nn
    :type txt_search: string
    :param ref_date: reference date given as datetime. Defaults to None
    :type ref_date: string, optional
    :return: return a datetime if expression valid, otherwise None
    :rtype: datetime
    """
    date_ = None
    m = re.match(
        '(20[0-9][0-9])-((0[1-9])|(1[0-2]))-(0[1-9]|[1-2][0-9]|3[0-1])$', txt_search)
    if m is None:
        m = re.match('(today)([+\-]?\d*)$', txt_search)
        if m is not None:  # m[0] != m[1] and
            date_ = datetime.datetime.combine(
                datetime.date.today() + datetime.timedelta(days=int(m[2] or 0)), datetime.datetime.min.time())  # int(m[2])
            return date_
    # date_ = datetime.strptime(m[0], '%Y-%m-%d')
    # date_ = local_tz.localize(date_).astimezone(utc_tz)
    return parse_date(txt_search)


def parse_date(date):
    """ util for parsing timestamps from string to datetime object.

        input:
            date (str) : Date on the form "%m/%d/%Y %H:%M %p"
        Output:
            date (datetime object)
    """
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M %p")
    except:
        try:
            return datetime.datetime.strptime(date, "%m/%d/%Y %H:%M %p")
        except:
            try:
                return datetime.datetime.strptime(date, "%d.%m.%Y %H:%M")
            except:
                try:
                    return datetime.datetime.strptime(date, "%Y-%m-%d")
                except:
                    try:
                        return datetime.datetime.strptime(date, "%d.%m.%Y")
                    except:
                        raise Exception("Error parsing datestring")
                    

def convert_ft(value, target_unit):
    with open('resources/conversion_factors.json', 'r') as json_file:
        conversion_factors = json.load(json_file)['feet']

    if target_unit not in conversion_factors.keys():
        print("target unit not supported, returning ft value")
        return value
    
    return value * conversion_factors[target_unit]


if __name__ == '__main__':
    pass