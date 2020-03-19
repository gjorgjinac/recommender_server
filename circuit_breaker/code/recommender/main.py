
import time
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

from caller_service import CallerService

callerService = CallerService()

for i in range(0,12):
    print('----------CALL {0}----------'.format(i))
    try:
        callerService.requestData()
    except Exception as ex: pass

    if i == 7:
        Popen([executable, 'call_remote.py'], creationflags=CREATE_NEW_CONSOLE)
    time.sleep(4)
    print()
