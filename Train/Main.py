from Train.Trn import *
from Train.passenger import *

train = Trn()
while 1:
    command = input('输入命令')
    command = command.upper()
    if command == 'INIT':
        train.init()
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
    elif command == 'Exit' or command == 'exit':
        break
    else:
        print('指令错误!')
