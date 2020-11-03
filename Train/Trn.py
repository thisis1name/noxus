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
        self.location = 0
        self.milleage = 0
        self.income = 0.0
        print('初始化成功')

    def myprint(self):
        print(self.current_Time)

    def HCCX(self):
        print('当前系统时间' + self.gettime(self.current_Time))
        print('候车人数' + str(len(self.passengers_Waiting)))
        print('候车乘客:')
        for passenger in self.passengers_Waiting:
            print(passenger.Passenger_Id)

    def HC(self, passenger, time):
        if time > 2400 or time < 0 or time % 100 > 59:
            print('时间错误')
        elif self.passenger_isexist(passenger):
            print('已有该乘客')
        else:
            # 求出要去的方向
            passenger.direction = Site.SITES.index(passenger.site_End) - Site.SITES.index(passenger.site_Start)
            if passenger.direction > 0:
                passenger.direction = 1
            else:
                passenger.direction = -1
            if time == (self.current_Time or self.current_Time == 730) and time < 730 \
                    and ((time % 10) == 0) and (passenger.direction == self.sites[self.location].direction
                         and passenger.site_Start == self.sites[self.location].site_From):  # 判断是否可以直接上车
                passenger.time_intrain = self.current_Time
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
                        self.milleage += self.getduration(site.time_arrive, self.current_Time)
                        self.getout_running(site)  # 下车
                        self.getin_running(site)  # 上车
                        self.current_Time = site.time_arrive
                    else:  # 未能过站
                        self.milleage += time - self.current_Time
                        for passenger in self.passengers:
                            passenger.mileage += self.getduration(time, self.current_Time)
                        self.current_Time = time
                        break
                else:  # 在停车
                    self.getin_waiting(site)
                    if time >= site.time_arrive:
                        for passenger in self.passengers:
                            if passenger.site_Start == site.site_From:
                                passenger.time_Waiting = self.getduration(site.time_arrive, passenger.time_intrain)
                            else:
                                passenger.time_Waiting += self.getduration(site.time_arrive, self.current_Time)
                        self.current_Time = site.time_arrive
                    else:  # 未能发车
                        for passenger in self.passengers:
                            if passenger.site_Start == site.site_From:
                                passenger.time_Waiting = self.getduration(time, passenger.time_Starting)
                            else:
                                passenger.time_Waiting += self.getduration(time, self.current_Time)
                        self.current_Time = time
                        break
            self.location = int(self.getduration(time, 730) / 10)
            if self.location > len(self.sites) - 1:
                self.location = len(self.sites) - 1
        else:
            if self.current_Time < 2130:
                self.settime(2129)
                self.milleage += 1
            for passenger in self.passengers:
                passenger.mileage += 1
                passenger.time_Ending = 2130
                self.passengers_Arrived.append(passenger)
                self.passengers.remove(passenger)
            self.current_Time = time

    def CXZD(self, id_temp):
        isarrived = 0
        for passenger in self.passengers_Arrived:
            if passenger.Passenger_Id == id_temp:
                print('系统当前时间' + self.gettime(self.current_Time))
                print('乘客编号: ' + str(passenger.Passenger_Id))
                print('上车站点: ' + str(passenger.site_Start))
                print('下车站点: ' + str(passenger.site_End))
                print('候车时刻: ' + self.gettime(passenger.time_Starting))
                print('上车时刻: ' + self.gettime(passenger.time_intrain))
                print('下车时刻: ' + self.gettime(passenger.time_Ending))
                print('乘车里程: ' + str(passenger.mileage))
                print('停车等候时间: ' + str(passenger.time_Waiting) + '分钟')
                print('金额" ' + str(passenger.cost))
                isarrived = 1
        if isarrived == 0:
            print('未查到该乘客或还未下车')
        return

    def HCZT(self):
        print('系统当前时间: ' + self.gettime(self.current_Time))
        print('当前位置: ' + self.sites[self.location].site_From + '---' + self.sites[self.location].site_To)
        # print('当前位置: ' + str(self.location) + '---' + str(self.location))
        print('当前状态: ' + ('停车等候' if self.sites[self.location].iswaiting else '匀速行驶'))
        print('当前乘客人数: ' + str(len(self.passengers)))
        print('形式总里程: ' + str(self.milleage))
        print('当前总收入: ' + str(self.income))

    def getincome(self):
        self.income = 0
        for passenger in self.passengers:
            mileage = passenger.mileage + passenger.time_Waiting / 5
            if mileage > 10:
                passenger.cost = 10 + (mileage - 10) * 1.5
            else:
                passenger.cost = 10
            self.income += passenger.cost
        for passenger in self.passengers_Arrived:
            mileage = passenger.mileage + passenger.time_Waiting / 5
            passenger.cost = 10 + (mileage - 10) * 1.5
            self.income += passenger.cost

    def getin_running(self, site):
        passenger_temp = []
        for passenger in self.passengers_Waiting:  # 是否上车
            if passenger.site_Start == site.site_To and passenger.direction == site.direction \
                    and passenger.time_Starting <= site.time_arrive:
                self.passengers.append(passenger)
                passenger_temp.append(passenger)
                passenger.time_intrain = site.time_arrive
        for passenger in passenger_temp:
            self.passengers_Waiting.remove(passenger)

    def getout_running(self, site):
        passenger_temp = []
        for passenger in self.passengers:  # 是否下车
            passenger.mileage += self.getduration(site.time_arrive, self.current_Time)
            if passenger.site_End == site.site_To:
                self.passengers_Arrived.append(passenger)
                passenger_temp.append(passenger)
                passenger.time_Ending = site.time_arrive
        for passenger in passenger_temp:
            self.passengers.remove(passenger)

    def getin_waiting(self, site):
        passenger_temp = []
        for passenger in self.passengers_Waiting:
            if passenger.site_Start == site.site_From and passenger.direction == site.direction:
                self.passengers.append(passenger)
                passenger_temp.append(passenger)
                passenger.time_intrain = passenger.time_Starting
        for passenger in passenger_temp:
            self.passengers_Waiting.remove(passenger)

    @staticmethod
    def getduration(time_now, time_ago):
        hour = int(time_now / 100) - int(time_ago / 100)
        minute = time_now % 100 - time_ago % 100
        return 60 * hour + minute

    @staticmethod
    def gettime(time):
        minute = time % 100
        return str(int(time / 100)) + ':' + ('0' + str(minute) if minute < 10 else str(minute))

    def passenger_isexist(self, passenger):
        for passenger1 in self.passengers:
            if passenger.Passenger_Id == passenger1.Passenger_Id:
                return True
        for passenger1 in self.passengers_Waiting:
            if passenger.Passenger_Id == passenger1.Passenger_Id:
                return True
        for passenger1 in self.passengers_Arrived:
            if passenger.Passenger_Id == passenger1.Passenger_Id:
                return True
        return False


