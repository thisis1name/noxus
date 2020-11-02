SITES = ['WA']
for i in range(1, 11):
    SITES.append('W' + str(i))
SITES.append('WB')
# print(SITES)

waiting = (1310, 1440, 1610, 1640, 1910, 1940, 2010)

class Site:
    site_From = ''
    site_To = ''
    time_arrive = 0
    iswaiting = 0
    direction = 0  # 路线方向

    def __init__(self, time, site1, site2, iswaiting, direction):
        self.site_From = site1
        self.site_To = site2
        self.time_arrive = time
        self.iswaiting = iswaiting
        self.direction = direction


def getSites():
    sites = []
    time = 740
    while time <= 2130:
        for i in range(11):
            if time > 2130:
                break
            if waiting.count(time) > 0:
                sites.append(Site(time, SITES[i], SITES[i + 1],1, 1))
                time += 10
                if time % 100 == 60:
                    time += 100
                    time -= 60
            else:
                sites.append(Site(time, SITES[i], SITES[i + 1], 0, 1))
            time += 10
            if time % 100 == 60:
                time += 100
                time -= 60
        for i in range(11,0,-1):
            if time > 2130:
                break
            if waiting.count(time) > 0:
                sites.append(Site(time, SITES[i], SITES[i - 1], 1, 1))
                time += 10
                if time % 100 == 60:
                    time += 100
                    time -= 60
            else:
                sites.append(Site(time, SITES[i], SITES[i - 1], 0, -1))
            time += 10
            if time % 100 == 60:
                time += 100
                time -= 60
    return sites

