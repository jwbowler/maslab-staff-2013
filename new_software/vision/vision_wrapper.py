from multiprocessing import Process, Pipe
import maslab_vision, time, sys

class VisionModule:

    def __init__(self):
        self.x = None
        self.y = None
        self.numObjects = 0
        self.data = None
        self.frameID = -1
        self.timestamp = None
	
    def start(self):
        balltracking.setup()
        self.conn_Py2Cv, self.conn_Cv2Py = Pipe()
        self.p = Process(target=f, args=(self.conn_Cv2Py,))
        self.p.start()
        print "Vision thread started"
		
    def update(self):
        conn = self.conn_Py2Cv
        if (not conn.poll()):
            return False
        while (conn.poll()):
            (self.timestamp, data) = conn.recv()
        self.frameID = data[0]
        data = [obj for obj in data[1:] if obj[0] != '']
        self.numObjects = len(self.data)
        return True
	
    def stop(self):
        conn = self.conn_Py2Cv
        conn.close()
        self.p.terminate()
        self.p.join()
	
    def getFrameID(self):
        return self.frameID
        
    def getTimestamp(self):
        return self.timestamp
        
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
            data = balltracking.step()
            timestamp = time.time()
            conn.send((time, data))
    except KeyboardInterrupt:
        pass
        
