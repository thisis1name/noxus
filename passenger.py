class Passenger :
    Passenger_Id = ''
    site_Start = ''
    site_End = ''
    time_Waiting = 0
    time_Starting = 0
    time_Ending = 0
    mileage = 0
    cost = 10.0
    direction = 0
    time_intrain = 0

    def __init__(self, id , time_Starting, site_Start, site_End):
        self.Passenger_Id = id
        self.site_Start = site_Start
        self.site_End = site_End
        self.time_Starting = time_Starting
