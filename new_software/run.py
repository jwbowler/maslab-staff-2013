import commander
import signal
import sys
import config

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

try:
    signal.signal(signal.SIGALRM, alarm_handler)
    if config.TIME_BEFORE_HALT > 0:
        signal.alarm(config.TIME_BEFORE_HALT)
    commander.go()    
except (KeyboardInterrupt, Alarm):
    commander.stop()
