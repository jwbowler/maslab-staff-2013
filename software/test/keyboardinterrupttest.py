from vision_interface import VisionInterface
import sys

def main():
    global vi
    vi = VisionInterface()
    i = 0
    while (i < 30):
        print vi.get()
        print i
        i += 1
    del(vi)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        global vi
        del(vi)
        sys.exit(0)
