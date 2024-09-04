class Windmill:

    def __init__(self, height_m, blade_length_m, cap_mw, p50):
        self.height = height_m
        self.blade_length = blade_length_m
        self.cap_mw = cap_mw
        self.p50 = p50

    def __str__(self):
        return f"\n Windmill with height {self.height} m and blade length {self.blade_length} m, producing up to {self.cap_mw} MW."
    
class WindPark:

    def __init__(self, n_mills, mill, location = 'None'):

        self.location = location if location is not None else "unknown"
        self.n_mills = n_mills
        self.mill_type = mill
        self.cap_mw = n_mills * mill.cap_mw

    def __str__(self):
        return f"\n Wind park with {self.n_mills}, located at {self.location} with mill type: \n {self.mill_type.__str__()} \n Total capacity: {self.cap_mw} MW."