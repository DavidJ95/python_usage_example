import datetime
import json


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