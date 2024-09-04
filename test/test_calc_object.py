import calc_object

def test_windpark():

    mill = calc_object.Windmill(height_m = 100, blade_length_m = 30, cap_mw = 5, p50 = 2)
    print(mill)

    park = calc_object.WindPark(n_mills = 10, mill = mill, location = 'Djursland')
    print(park)

test_windpark()