#include "vision.h"
#include <unistd.h>
#include <sys/time.h>

int cameraID;
double downsampleFactor;
string *colorNames;
bool *colorEnableFlags;
int numColors;
int **colorThresholds;
int *wallStripeThresholds;
int gapWidthThreshold;

Mat src;
Mat ds;
Mat hsv;
Mat bw;
Mat colors;
Mat colors3c;
Mat temp;
Mat wallMap;
SimpleBlobDetector::Params params;
cv::Ptr<FeatureDetector> blob_detector;
vector<KeyPoint> keyPoints;
struct timeval startTime, endTime;
long seconds, useconds;
double mtime;

int frameCount = 0;

string objTypes[16];
int objXCoords[16];
int objYCoords[16];
int objSizes[16];
bool objIsBehindWall[16];

VideoCapture cap;

//VideoWriter rgbRecord("recordedRGB.mpeg", CV_FOURCC('P', 'I', 'M', '1'), 30, Size(640, 480));
//VideoWriter blobRecord("recordedBlobs.mpeg", CV_FOURCC('P', 'I', 'M', '1'), 30, Size(640, 480));

Config cfg;

string convertInt(int number) {
   stringstream ss;
   ss << number;
   return ss.str();
}

int setup() {
    load_params();
	init_opencv();
	return 0;
}

int load_params() {
    try {
        cfg.readFile("visionparams.cfg");
    } catch (FileIOException &e) {
        cout << "Config file I/O error" << endl;
        return EXIT_FAILURE;
    } catch (ParseException &e) {
        cout << "Parse error at visionparams.cfg:"
             << e.getLine() << " - " << e.getError() << endl;
        return EXIT_FAILURE;
    }

    cfg.lookupValue("camera", cameraID);
    cfg.lookupValue("downsampleFactor", downsampleFactor);

    numColors = cfg.lookup("colors").getLength();
    cout << "numColors: " << numColors << endl;
    colorNames = new string[numColors];
    colorEnableFlags = new bool[numColors];
    colorThresholds = new int*[numColors];    
    Setting &colorsGroup = cfg.lookup("colors");
    for (int i = 0; i < numColors; i++) {
        colorThresholds[i] = new int[6];
        Setting &colorInfo = colorsGroup[i];
        colorInfo.lookupValue("name", colorNames[i]);
        colorInfo.lookupValue("enabled", colorEnableFlags[i]);
        colorInfo.lookupValue("hueMin", colorThresholds[i][0]);
        colorInfo.lookupValue("hueMax", colorThresholds[i][1]);
        colorInfo.lookupValue("satMin", colorThresholds[i][2]);
        colorInfo.lookupValue("satMax", colorThresholds[i][3]);
        colorInfo.lookupValue("valMin", colorThresholds[i][4]);
        colorInfo.lookupValue("valMax", colorThresholds[i][5]);
    }

    wallStripeThresholds = new int[numColors];
    Setting &wallStripeColors = cfg.lookup("wallStripeColor");
    wallStripeColors.lookupValue("hueMin", wallStripeThresholds[0]);
    wallStripeColors.lookupValue("hueMax", wallStripeThresholds[1]);
    wallStripeColors.lookupValue("satMin", wallStripeThresholds[2]);
    wallStripeColors.lookupValue("satMax", wallStripeThresholds[3]);
    wallStripeColors.lookupValue("valMin", wallStripeThresholds[4]);
    wallStripeColors.lookupValue("valMax", wallStripeThresholds[5]);
    cfg.lookupValue("gapWidthThreshold", gapWidthThreshold);

    return 0;
}
  	
int init_opencv() {

    cap = VideoCapture(cameraID);
	
    if(!cap.isOpened())  // check if we succeeded
        return -1;
    
    // to initialize colors to the right size:
    cap.set(CV_CAP_PROP_FRAME_WIDTH, 640*downsampleFactor);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, 480*downsampleFactor);
    cap.set(CV_CAP_PROP_FPS, 30);
    cap.set(CV_CAP_PROP_POS_FRAMES, 0);
    cap >> src;
    colors.create(src.size(), CV_8U);
    
    params.minDistBetweenBlobs = 0.;
    params.filterByInertia = false;
    params.filterByConvexity = false;
    params.filterByColor = true;
    params.blobColor = 255;
    params.filterByCircularity = false;
    params.filterByArea = true;
    params.minArea = 5.;
    params.maxArea = 640.*480;
    
    blob_detector = new cv::SimpleBlobDetector(params);
    blob_detector->create("SimpleBlob");
    
    gettimeofday(&startTime, NULL);

    return 0;
} 

int step(bool isCalibMode, Mat **frame_ptr, Mat **scatter_ptr, int colorBeingCalibrated) {

    //gettimeofday(&startTime, NULL);
    cap.grab();
    cap.retrieve(src);
    gettimeofday(&endTime, NULL);
    //usleep(50000);

    seconds = endTime.tv_sec - startTime.tv_sec;
    useconds = endTime.tv_usec - startTime.tv_usec;
    mtime = (seconds + useconds/1000000.);
    if (frameCount % 10 == 0) {
        //cout << mtime << endl;
        //cout << 1/mtime << endl;
    }
    startTime = endTime;
    frameCount++;
    //return 0;

    cvtColor(src, hsv, CV_BGR2HSV);
    colors.setTo(Scalar(0));
    
    int numDetections = 0;
    for (int i = 0; i < maxDetections; i++) {
        objTypes[i] = "";
        objXCoords[i] = 0;
        objYCoords[i] = 0;
        objSizes[i] = 0;
        objIsBehindWall[i] = false;
    }

    int numCycles;
    if (isCalibMode) {
        numCycles = 1;
    } else {
        numCycles = numColors;
    }

    updateWallMap();

    for (int i = 0; i < numCycles; i++) {

        if (!colorEnableFlags[i] && !isCalibMode) {
            continue;
        }

        if (numDetections >= maxDetections) {
            break;
        }

        int colorIndex;
        if (isCalibMode) {
            colorIndex = colorBeingCalibrated;
        } else {
            colorIndex = i;
        }
        
        int *t = colorThresholds[colorIndex];

        //cout << t[0] << " " << t[1] << " " << t[2] << " "
        //     << t[3] << " " << t[4] << " " << t[5] << endl;
        if (t[0] >= 0) {
            inRange(hsv, Scalar(t[0], t[2], t[4]), Scalar(t[1], t[3], t[5]), bw);
        } else {
            int t_0 = 180 + t[0];
            inRange(hsv, Scalar(t_0, t[2], t[4]), Scalar(180, t[3], t[5]), bw);
            inRange(hsv, Scalar(0, t[2], t[4]), Scalar(t[1], t[3], t[5]), temp);
            bitwise_or(bw, temp, bw);
        }
        bitwise_or(colors, bw, colors);
        
        blob_detector->detect(bw, keyPoints);

        for (int j = 0; j < keyPoints.size(); j++) {
            double scale = 1/downsampleFactor;
            int x = keyPoints[j].pt.x;
            int y = keyPoints[j].pt.y;
	    objTypes[numDetections] = colorNames[colorIndex];
            objXCoords[numDetections] = x * scale;
            objYCoords[numDetections] = y * scale;
            objSizes[numDetections] = keyPoints[j].size;
            objIsBehindWall[numDetections] = isBehindWall(x, y);
            numDetections++;
            if (numDetections == maxDetections) {
                break;
            }
        }
        //cout << endl;
        
    }

    int out = 0;
    /* 
    cvtColor(colors, colors3c, CV_GRAY2BGR);
    string frameCountStr = convertInt(frameCount);
    putText(colors3c, frameCountStr, cvPoint(5,15),
            FONT_HERSHEY_COMPLEX_SMALL, 0.8, Scalar(0,255,0));
    putText(src, frameCountStr, cvPoint(5,15),
            FONT_HERSHEY_COMPLEX_SMALL, 0.8, Scalar(0,255,0));
    */ 
    if (frame_ptr != NULL) {
        *frame_ptr = &src;
    }
    if (scatter_ptr != NULL) {
        //*scatter_ptr = &colors3c;
	*scatter_ptr = &colors;
    }
    
    //rgbRecord << src;
    //blobRecord << colors3c;
    
    return out;   
}

void updateWallMap() {
    cap >> src;
    cvtColor(src, hsv, CV_BGR2HSV);
    int *t = wallStripeThresholds;
    inRange(hsv, Scalar(t[0], t[2], t[4]), Scalar(t[1], t[3], t[5]), wallMap);
}

void getWallImages(Mat **frame_ptr, Mat **scatter_ptr) {
    updateWallMap();
    *frame_ptr = &src;
    *scatter_ptr = &wallMap;
}

bool isBehindWall(int pixelX, int pixelY) {
    int wImg = wallMap.size().width;
    int hImg = wallMap.size().height;
    int x = pixelX - gapWidthThreshold;
    int y = pixelY;
    int w = gapWidthThreshold*2 + 1;
    int h = hImg - pixelY;
    if (h < 1) {
        return false;
    }
    if (x < 0) {
        x = 0;
    }
    if (x + w >= wImg) {
        x -= x + w + 1 - wImg;
    }
    //cout << "(" << x << ", " << y << "), (" << x + w << ", " << y + h << ")" << endl;

    //try {
        Rect roi(x, y, w, h);
        Mat wallMapROI = wallMap(roi);
        bool out = (bool) countNonZero(wallMapROI);
        //cout << out << endl;
        return out;
    //} catch (cv::Exception &e) {
        //return false;
    //}
}
