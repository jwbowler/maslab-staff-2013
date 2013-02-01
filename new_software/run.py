import commander
import signal
import sys
import config

try:
    commander.go()    

except (KeyboardInterrupt):
    pass

'''
except:
    commander.stop()
    print sys.exc_info()
'''

commander.stop()
