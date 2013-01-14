from multiprocessing import Process, Pipe
import balltracking, time, sys

SIG_STOP = 0
	

class BallTracker:

    def __init__(self):
        self.x = None
        self.y = None
        #self.isObject = 0
        self.numObjects = 0
        self.data = None
        self.frameID = -1
	
    def start(self):
        balltracking.setup()
        self.conn_Py2Cv, self.conn_Cv2Py = Pipe()
        self.p = Process(target=f, args=(self.conn_Cv2Py,))
        self.p.start()
        print "Vision thread started"
		
    def update(self):
        conn = self.conn_Py2Cv
        data = conn.recv()
        while (conn.poll()):
            data = conn.recv()

        '''
        if data != 0:
            self.isObject = 1
        else:
            self.isObject = 0
        self.x = data / 480
        self.y = data % 480
        print data
        return data
        '''
        self.frameID = data[0]
        data = data[1:]
        clean = [obj for obj in data if obj[0] != '']
        self.data = clean
        self.numObjects = len(self.data)
	
    def stop(self):
        conn = self.conn_Py2Cv
        #conn.send(SIG_STOP)
        conn.close()
        self.p.terminate()
        self.p.join()
	
    def getFrameID(self):
        return self.frameID
        
    def getNumObj(self):
        return self.numObjects

    def getType(self, i):
        return self.data[i][0]
        
    def getX(self, i):
        return self.data[i][1]

    def getY(self, i):
        return self.data[i][2]
        
    def getWeight(self, i):
        return self.data[i][3]
		
def f(conn):
    try:
        while (True):
            #print "Running"
            #if conn.poll():
            #    sig = conn.recv()
            #    if sig == SIG_STOP:
            #        print "Closing"
            #        conn.close()
            #        return;
            data = balltracking.step()
            conn.send(data)
    except KeyboardInterrupt:
        pass
        
