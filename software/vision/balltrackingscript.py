from multiprocessing import Process, Pipe
import balltracking, time

SIG_STOP = 0
	

class BallTracker:

    def __init__(self):
        self.x = None
        self.y = None
        self.isObject = 0
	
    def start(self):
        balltracking.setup()
        self.conn_Py2Cv, self.conn_Cv2Py = Pipe()
        self.p = Process(target=f, args=(self.conn_Cv2Py,))
        self.p.start()
        print "Started"
		
    def update(self):
        conn = self.conn_Py2Cv
        data = conn.recv()
        while (conn.poll()):
            data = conn.recv()
	    
        if data != 0:
            self.isObject = 1
        else:
            self.isObject = 0
        self.x = data / 480
        self.y = data % 480
	
    def stop(self):
        conn = self.conn_Py2Cv
        conn.send(SIG_STOP)
        conn.close()
        self.p.join()
	
    #The following are incomplete
    def getNumObj(self):
        return self.isObject
	
    def getX(self, i):
        return self.x

    def getY(self, i):
        return self.y
	
    def getType(self, i):
        return "RED_BALL"
		
def f(conn):
	while (True):
		if conn.poll():
			sig = conn.recv()
			if sig == SIG_STOP:
				conn.close()
				return;
		data = balltracking.step()
		conn.send(data)
	
'''
bt = BallTracker()
bt.start()
for i in range(20):
	time.sleep(1)
	print bt.update()
bt.stop()
'''

	
	

    
    
