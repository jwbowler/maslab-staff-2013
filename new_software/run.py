import commander
import signal
import sys

try:
    commander.go()    
except (KeyboardInterrupt, Alarm):
    commander.stop()
