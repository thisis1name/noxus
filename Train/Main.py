from Train.Trn import *
from Train.passenger import *

train = Trn()


def printcommands():
    print('指令示例(不区分大小写)')
    print('初始化 Init')
    print('候车命令  HC CK01 07:20 WA W4')
    print('查询以下车的乘客账单 CXZD CK01')
    print('火车状态查询  HCZD')
    print('候车查询  HCCX')
    print('仅设定系统时间  SETTIME 07:30')


while 1:
    printcommands()
    command = input('输入命令:  ')
    command = command.upper()
    if command == 'INIT':
        train.init()
    elif command.startswith('SETTIME'):
        strs = command.split(' ')
        if len(strs) == 2:
            times = strs[1].split(':')
            time = int(times[0]) * 100 + int(times[1])
            if time > train.current_Time:
                train.settime(time)
                train.getincome()
        else:
            print('指令错误')
    elif command == 'HCCX':
        train.HCCX()
    elif command == 'HCZT':
        train.HCZT()
    elif command.startswith('HC'):
        strs = command.split(' ')
        if len(strs) == 5:
            times = strs[2].split(':')
            time = int(times[0]) * 100 + int(times[1])
            train.HC(Passenger(strs[1], time, strs[3], strs[4]), time)
        else:
            print('指令错误!')
    elif command.startswith('CXZD'):
        strs = command.split()
        if len(strs) == 2:
            train.CXZD(strs[1])
        else:
            print('指令错误!')
    elif command == 'EXIT':
        break
    else:
        print('指令错误!')
