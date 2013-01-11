from multiprocessing import Process, Pipe
import time

def f(conn):
    for i in range(100):
        cSend.send(i)
        time.sleep(0.1)
    conn.close()

if __name__ == '__main__':
    cRecv, cSend = Pipe(False)
    p = Process(target=f, args=(cSend,))
    p.start()
    for i in range(5):
        blah = cRecv.recv()
        while (cRecv.poll()):
            blah = cRecv.recv()
        print blah
        time.sleep(1)
    p.join()
