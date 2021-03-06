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
Mat goalMap;
SimpleBlobDetector::Params params;
cv::Ptr<FeatureDetector> blob_detector;
vector<KeyPoint> keyPoints;
struct timeval startTime, endTime;
long seconds, useconds;
double mtime;

int frameCount = 0;

string objTypes[16];
int objXCenters[16];
int objYCenters[16];
Rect objBoxes[16];
int objSizes[16];
int objXLowestPoints[16];
int objYLowestPoints[16];
bool objIsBehindWall[16];
bool objIsInGoal[16];

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
    params.minArea = 5;
    params.maxArea = 640.*480;
    
    //blob_detector = new cv::SimpleBlobDetector(params);
    //blob_detector->create("SimpleBlob");
    
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
        //objXCoords[i] = 0;
        //objYCoords[i] = 0;
        //objSizes[i] = 0;
        //objIsBehindWall[i] = false;
    }

    int numCycles;
    if (isCalibMode) {
        numCycles = 1;
    } else {
        numCycles = numColors;
    }

    updateWallMap();
    updateGoalMap();

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

        // assumes that BLUE_GOAL is the third from the top of the config color list
        if (i == 2) {
            Mat topMask = colors.clone();
            topMask.setTo(Scalar(0));
            rectangle(topMask, Point(0, 0), Point(topMask.size().width, 3), Scalar(255), CV_FILLED);
            bitwise_and(bw, topMask, bw);
        }
        /*
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
        */
        vector<Point2d> centers;
        vector<Rect> boxes;
        vector<int> areas;
        vector<Point2d> lowestPoints;
        //blob_detector->detect(bw, keyPoints);
        findBlobs(bw, centers, boxes, areas, lowestPoints);

        int max_index = max_element(areas.begin(),areas.end()) - areas.begin();

        for (int j = 0; j < centers.size(); j++) {
            ///
            if (j != max_index) {
                continue;
            }
            ///
            double scale = 1/downsampleFactor;
            double scaleSq = scale*scale;
            int x = centers[j].x;
            int y = centers[j].y;
            int xL = lowestPoints[j].x;
            int yL = lowestPoints[j].y;
            objTypes[numDetections] = colorNames[colorIndex];
            objXCenters[numDetections] = x * scale;
            objYCenters[numDetections] = y * scale;
            objBoxes[numDetections] = boxes[j];
            //objSizes[numDetections] = areas[j] * scaleSq;
            objSizes[numDetections] = areas[j];
            objXLowestPoints[numDetections] = xL * scale;
            objYLowestPoints[numDetections] = yL * scale;
            objIsBehindWall[numDetections] = isBehindWall(x, y);
            objIsInGoal[numDetections] = isInGoal(x, y);
            numDetections++;
            if (numDetections == maxDetections) {
                break;
            }
        }

        
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
    cvtColor(src, hsv, CV_BGR2HSV);
    int *t = wallStripeThresholds;
    inRange(hsv, Scalar(t[0], t[2], t[4]), Scalar(t[1], t[3], t[5]), wallMap);
}

void updateGoalMap() {
    Mat goalMap1;
    Mat temp;
    // add purple goal to wall map
    int *t = colorThresholds[0];
    if (t[0] >= 0) {
        inRange(hsv, Scalar(t[0], t[2], t[4]), Scalar(t[1], t[3], t[5]), goalMap1);
    } else {
        int t_0 = 180 + t[0];
        inRange(hsv, Scalar(t_0, t[2], t[4]), Scalar(180, t[3], t[5]), goalMap1);
        inRange(hsv, Scalar(0, t[2], t[4]), Scalar(t[1], t[3], t[5]), temp);
        bitwise_or(goalMap1, temp, goalMap1);
    }
    // add yellow wall to wall map
    Mat goalMap2;
    t = colorThresholds[1];
    inRange(hsv, Scalar(t[0], t[2], t[4]), Scalar(t[1], t[3], t[5]), goalMap2);
    bitwise_or(goalMap1, goalMap2, goalMap);
}    

void getWallImages(Mat **frame_ptr, Mat **scatter_ptr) {
    cap >> src;
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

    Rect roi(x, y, w, h);
    Mat wallMapROI = wallMap(roi);
    bool out = (bool) countNonZero(wallMapROI);
    return out;
}

bool isInGoal(int pixelX, int pixelY) {
    int wImg = goalMap.size().width;
    int hImg = goalMap.size().height;
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

    Rect roi(x, y, w, h);
    Mat goalMapROI = goalMap(roi);
    bool out = (bool) countNonZero(goalMapROI);
    return out;
}

void findBlobs(const cv::Mat &binaryImage, vector<Point2d> &centers, vector<Rect> &boxes, vector<int> &areas, vector<Point2d> &lowestPoints) {
    centers.clear();

    vector < vector<Point> > contours;
    Mat tmpBinaryImage = binaryImage.clone();
    findContours(tmpBinaryImage, contours, CV_RETR_LIST, CV_CHAIN_APPROX_NONE);

    for (size_t contourIdx = 0; contourIdx < contours.size(); contourIdx++)
    {
        Moments moms = moments(Mat(contours[contourIdx]));
        
        double area = moms.m00;
        if (area < params.minArea || area >= params.maxArea)
            continue;

        Point2d center = Point2d(moms.m10 / moms.m00, moms.m01 / moms.m00);

        if (binaryImage.at<uchar> (cvRound(center.y), cvRound(center.x)) != params.blobColor)
            continue;

        Rect box = boundingRect(contours[contourIdx]);

        //compute blob radius
        vector<double> dists;
        Point2d lowestPoint(0, 0);
        for (size_t pointIdx = 0; pointIdx < contours[contourIdx].size(); pointIdx++)
        {
            Point2d pt = contours[contourIdx][pointIdx];
            dists.push_back(norm(center - pt));
            if (pt.y > lowestPoint.y) {
                lowestPoint.x = pt.x;
                lowestPoint.y = pt.y;
            }
        }
        std::sort(dists.begin(), dists.end());
        int size = (dists[(dists.size() - 1) / 2] + dists[dists.size() / 2]) / 2.;

        centers.push_back(center);
        boxes.push_back(box);
        areas.push_back(area);
        lowestPoints.push_back(lowestPoint);
    }
}
