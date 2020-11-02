from Train import Site


class Trn:
    current_Time = 730
    passengers = []
    passengers_Waiting = []
    passengers_Arrived = []
    sites = []
    location = 0
    milleage = 0
    income = 0.0

    def __init__(self):
        self.sites = Site.getSites()

    def init(self):
        self.current_Time = 730
        self.passengers.clear()
        self.passengers_Waiting.clear()
        self.passengers_Arrived.clear()
        self.sites = []
        self.location = 0
        self.milleage = 0
        self.income = 0.0
        print('初始化成功')

    def myprint(self):
        print(self.current_Time)

    def HCCX(self):
        print('当前系统时间' + str(self.current_Time))
        print('候车人数' + str(len(self.passengers_Waiting)))
        print('候车乘客:')
        for passenger in self.passengers_Waiting:
            print(passenger.Passenger_Id)

    def HC(self, passenger, time):
        # 求出要去的方向
        passenger.direction = Site.SITES.index(passenger.site_End) - Site.SITES.index(passenger.site_Start)
        if passenger.direction > 0:
            passenger.direction = 1
        else:
            passenger.directiono = -1
        if time == self.current_Time or self.current_Time == 730 and time < 730 \
                and ((time % 10) == 0 or self.sites[self.location].iswaiting == 1) \
                and (passenger.direction == self.sites[self.location].direction \
                     and passenger.site_Start == self.sites[self.location].site_From):  # 判断是否可以直接上车
            self.passengers.append(passenger)
        else:
            self.passengers_Waiting.append(passenger)
        if time > self.current_Time:
            self.settime(time)
        self.getincome()
        print('操作成功')

    def settime(self, time):
        if time < 2130:
            for site in self.sites[self.location:]:
                if site.iswaiting == 0:  # 没在停车
                    if time >= site.time_arrive:  # 可以过站
                        self.milleage += site.time_arrive - self.current_Time
                        for passenger in self.passengers:  # 是否下车
                            passenger.mileage += site.time_arrive - self.current_Time
                            if passenger.site_End == site.site_To:
                                self.passengers_Arrived.append(passenger)
                                self.passengers.remove(passenger)
                                passenger.time_Ending = site.time_arrive
                        for passenger in self.passengers_Waiting:  # 是否上车
                            if passenger.site_Start == site.site_To and passenger.direction == site.direction:
                                self.passengers.append(passenger)
                                self.passengers_Waiting.remove(passenger)
                                passenger.time_intrain = site.time_arrive
                                passenger.time_intrain = site.time_arrive
                        self.current_Time = site.time_arrive
                    else:  # 未能过站
                        self.milleage += time - self.current_Time
                        for passenger in self.passengers:
                            passenger.mileage += time - self.current_Time
                        self.current_Time = time
                        break
                else:  # 在停车
                    if time >= site.time_arrive:
                        for passenger in self.passengers_Waiting:
                            if passenger.site_Start == site.site_From and passenger.direction == site.direction:
                                self.passengers.append(passenger)
                                self.passengers_Waiting.remove(passenger)
                                passenger.time_intrain = passenger.time_Starting
                        for passenger in self.passengers:
                            if passenger.site_Start == site.site_From:
                                passenger.time_Waiting = site.time_arrive - passenger.time_Starting
                            else:
                                passenger.time_Waiting += site.time_arrive - self.current_Time
                        self.current_Time = site.time_arrive
                    else:  # 为能发车
                        for passenger in self.passengers_Waiting:  # 是否能上车
                            if passenger.site_Start == site.site_From and passenger.direction == site.direction:
                                self.passengers.append(passenger)
                                self.passengers_Waiting.remove(passenger)
                                passenger.time_intrain = passenger.time_Starting
                        for passenger in self.passengers:
                            if passenger.site_Start == site.site_From:
                                passenger.time_Waiting = time - passenger.time_Starting
                            else:
                                passenger.time_Waiting += time - self.current_Time
                        self.current_Time = time
                        break
            self.location = int((time - 730) / 10)
            if self.location > len(self.sites) - 1:
                self.location = len(self.sites) - 1
        else:
            self.settime(2129)
            for passenger in self.passengers:
                self.milleage += 1
                passenger.mileage += 1
                passenger.time_Ending = 2130
                self.passengers_Arrived.append(passenger)
                self.passengers.remove(passenger)
            self.current_Time = time

    def CXZD(self, id):
        isarrived = 0
        for passenger in self.passengers_Arrived:
            if passenger.Passenger_Id == id:
                print('系统当前时间' + self.current_Time)
                print('乘客编号: ' + passenger.Passenger_Id)
                print('上车站点: ' + passenger.site_Start)
                print('下车站点: ' + passenger.site_End)
                print('候车时刻: ' + passenger.time_Starting)
                print('上车时刻: ' + passenger.time_intrain)
                print('下车时刻: ' + passenger.time_Ending)
                print('乘车里程: ' + passenger.mileage)
                print('停车等候时间: ' + passenger.time_Waiting)
                print('金额" ' + passenger.cost)
                isarrived = 1
        if isarrived == 0:
            print('未查到该乘客')
        return

    def HCZT(self):
        print('系统当前时间: ' + str(int(self.current_Time / 100)) + ':' + str(self.current_Time % 100))
        print('当前位置: ' + self.sites[self.location].site_From + '---' + self.sites[self.location].site_To)
        print('当前状态: ' + ('停车等候' if self.sites[self.location].iswaiting else '匀速行驶'))
        print('当前乘客人数: ' + str(len(self.passengers)))
        print('形式总里程: ' + str(self.milleage))
        print('当前总收入: ' + str(self.income))

    def getincome(self):
        self.income = 0
        for passenger in self.passengers:
            mileage = passenger.mileage + passenger.time_Waiting / 5
            if passenger.mileage > 10:
                passenger.cost = 10 + (passenger.mileage - 10) * 1.5
            else:
                passenger.cost = 10
            self.income += passenger.cost
        for passenger in self.passengers_Arrived:
            mileage = passenger.mileage + passenger.time_Waiting / 5
            passenger.cost = 10 + (passenger.mileage - 10) * 1.5
            self.income += passenger.cost
