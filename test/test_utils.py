import utils
import datetime

def test_parse_date():

    norwegian_date = '1.2.2021'
    date = utils.parse_date(norwegian_date)
    norwegian_date_back = datetime.datetime.strftime(date, format='%d.%m.%Y')

    pass

def test_convert_ft():

    dist_m = utils.convert_ft(3, 'm')
    dist_inches = utils.convert_ft(3, 'inches')
    dist_yards = utils.convert_ft(3, 'yards')
    dist_cm = utils.convert_ft(3, 'cm')

    dist_shmeet = utils.convert_ft(3, 'shmeet')

    pass

test_parse_date()
test_convert_ft()