from multiprocessing import Process, Pipe
import time, sys, vision

class VisionWrapper:

    # possible types (see getType()):
    # RED_BALL
    # GREEN_BALL
    # YELLOW_WALL
    # PURPLE_GOAL

    def __init__(self):
        self.x = None
        self.y = None
        self.numObjects = 0
        self.data = None
        self.frameID = -1
        self.timestamp = None
	
    def start(self):
        vision.setup()
        self.conn_Py2Cv, self.conn_Cv2Py = Pipe()
        self.p = Process(target=f, args=(self.conn_Cv2Py,))
        self.p.start()
		
    def update(self):
        conn = self.conn_Py2Cv
        if (not conn.poll()):
            return False
        while (conn.poll()):
            (self.timestamp, data) = conn.recv()
        self.frameID = data[0]
        self.data = [obj for obj in data[1:] if obj[0] != '']
        if self.data == None:
            self.numObjects = 0
        else:
            self.numObjects = len(self.data)
        return True
	
    def stop(self):
        print "stop"
        self.conn_Py2Cv.send('EXIT')
        self.p.join()
	
    def getFrameID(self):
        return self.frameID
        
    def getTimestamp(self):
        return self.timestamp
        
    def getNumObj(self):
        return self.numObjects

    def getType(self, i):
        return self.data[i][0]
        
        # returns list of integer indices of objects in received data
        # for which the object's type is <typeName>
    def getIndicesByType(self, typeName):
        return [i for i in xrange(self.numObjects)
                if self.data[i][0] == typeName]
        
    def getX(self, i):
        return self.data[i][1]

    def getY(self, i):
        return self.data[i][2]
        
    def getWeight(self, i):
        return self.data[i][3]

    def getIsBehindWall(self, i):
        return self.data[i][4]
		
def f(conn):
    while (True):
        try:
            if conn.poll():
                print "Received message"
                m = conn.recv()
                if m == 'EXIT':
                    print "Received EXIT"
                    break
            data = vision.step()
            timestamp = time.time()
            conn.send((timestamp, data))
        except KeyboardInterrupt:
            pass
        
if __name__ == '__main__':
    # test
    vw = VisionWrapper()
    vw.start()
    startTime = time.time()
    avgTime = 0
    try:
        while True:
            time.sleep(.01)
            if not vw.update():
                continue
            print vw.data
            endTime = time.time()
            duration = endTime - startTime
            startTime = endTime
            avgTime = 0.9*avgTime + 0.1*duration
            print 1/avgTime
            #print vw.getNumObj()
    except KeyboardInterrupt:
        vw.stop() 
