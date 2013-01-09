import cv, cv2, numpy, cPickle, time, random, math
import scipy.cluster.hierarchy as hcluster
import cProfile

#OpenCV HSV ranges: 0-180, 0-255, 0-255

pixelCounters = None

def run():

    print 1
    cv2.namedWindow("raw")
    cv2.namedWindow("scatter")
    #cv2.namedWindow("map")
    vc = cv2.VideoCapture(0)
    print 2

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False
        t = time.clock()

    global pixelCounters
    pixelCounters = numpy.empty(frame.shape, dtype=int)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            pixelCounters[i, j] = random.randint(1, 100)

    while rval:

        start = time.clock();

        #print 2.5

        dispImage = numpy.copy(frame)
        colors = numpy.empty(frame.shape, frame.dtype)
        mapImage = numpy.empty(frame.shape, frame.dtype)
        hsv = cv2.cvtColor(frame, cv.CV_BGR2HSV)
        #hsv = frame

        #print 3
        
        (data, clusters) = identify(hsv, colors)
        
##        if clusters != None:
##            draw_scatter(hsv, colors, data)
##            centers = draw_centers(dispImage, data, clusters)
##            create_map(centers, mapImage)
##            colors = cv2.cvtColor(colors, cv.CV_HSV2BGR)

        cv2.imshow("raw", dispImage)
        cv2.imshow("scatter", colors)
        #cv2.imshow("map", mapImage)
        
        rval, frame = vc.read()
        end = time.clock()
        key = cv2.waitKey(1)
        if key == 27: # exit on ESC
            break

    cv2.destroyAllWindows()


#########

def identify(image, colors):

    global pixelCounters

    num_colors = 1

    

    #data = numpy.zeros((1000,2))
    n = 0
    a = 0
    for x in xrange(0, image.shape[0]):
        for y in xrange(0, image.shape[1]):
            a += 1
            if a & 0b1111111 != 0:
                continue
            continue
            for i in range(num_colors):                
                hue = image[x, y, 0]
                sat = image[x, y, 1]
                val = image[x, y, 2]
                if hue >= 0 and hue < 10 and sat > 150 and val > 50:
                    data[n, 0] = x
                    data[n, 1] = y
                    n += 1
    if n < 2:
        return (None, None)
    
    t = 30
    data = data[0:n, :]
    clusters = hcluster.fclusterdata(data, t, criterion="distance")
    
    return (data, clusters)

def draw_scatter(image, colors, data):
    for i in range(data.shape[0]):
        colors[data[i, 0], data[i, 1], 0] = image[data[i, 0], data[i, 1], 0]
        colors[data[i, 0], data[i, 1], 1] = image[data[i, 0], data[i, 1], 1]
        colors[data[i, 0], data[i, 1], 2] = image[data[i, 0], data[i, 1], 2]

def draw_centers(image, data, clusters):
    m = clusters.max()
    xsums = [0] * m
    ysums = [0] * m
    sizes = [0] * m
    x = [0] * m
    y = [0] * m
    for i in range(0, data.shape[0]):
        c = clusters[i] - 1
        xsums[c] += data[i, 0]
        ysums[c] += data[i, 1]
        sizes[c] += 1
    for c in range(m):
        x[c] = int(xsums[c] / sizes[c])
        y[c] = int(ysums[c] / sizes[c])
        for i in range(-2, 3):
            for j in range(-2, 3):
                if x[c] + i < 0 or x[c] + i >= image.shape[0] \
                   or y[c] + j < 0 or y[c] + j >= image.shape[1]:
                    continue
                image[x[c] + i, y[c] + j, 0] = 0
                image[x[c] + i, y[c] + j, 1] = 255
                image[x[c] + i, y[c] + j, 2] = 0
    return (x, y)

def create_map(centers, map_image):
    angle = 30.
    height = .4
    vfov = 50.
    img_x_max = 640.
    img_y_max = 480.
    ar = img_x_max / img_y_max
    hfov = 50*ar

    min_angle = 90 - angle - vfov/2
    for i in range(0, len(centers[0])):
        x_img = centers[1][i]
        y_img = img_y_max - centers[0][i]
        y_real = height*math.tan(
            (2*math.pi/360)*(min_angle + (y_img/img_y_max)*vfov))
        diag_dist = math.sqrt(y_real*y_real + height*height)
        x_real = diag_dist*math.tan(
            (2*math.pi/360)*(hfov/2)*((x_img - img_x_max/2)/(img_x_max/2)))
        #print str(x_img) + ", " + str(y_img)
        #print str(x_real) + ", " + str(y_real)
        #print ""
        map_scale = 200
        x_map = x_real * map_scale + img_x_max/2
        y_map = img_y_max - y_real * map_scale
        for i in range(-2, 3):
            for j in range(-2, 3):
                if x_map + i < 0 or x_map + i >= img_x_max \
                   or y_map + j < 0 or y_map + j >= img_y_max:
                    continue
                map_image[y_map + i, x_map + j, 0] = 0
                map_image[y_map + i, x_map + j, 1] = 0
                map_image[y_map + i, x_map + j, 2] = 255
    #print ""


ra = 0x1ac57d3e
rb = 0x12345678
def rand(e): # returns True with probability 1/(2^e)
    global ra
    global rb
    ra += rb
    rb += 1
    return not (ra % (1 << (e-1)))

#for i in range(32):
#    print rand(5)
    
#cProfile.run('run()')
run()


