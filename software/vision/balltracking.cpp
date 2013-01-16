#include "balltracking.h"

Mat src;
Mat ds;
Mat hsv;
Mat bw[num_obj];
Mat colors;
Mat colors3c;
Mat temp;
SimpleBlobDetector::Params params;
cv::Ptr<FeatureDetector> blob_detector;
vector<KeyPoint> keyPoints;

int frameCount = 0;

string objTypes[16];
int objXCoords[16];
int objYCoords[16];
int objSizes[16];

VideoCapture cap(CAMERA);
VideoWriter rgbRecord("recordedRGB.mpeg", CV_FOURCC('P', 'I', 'M', '1'), 30, Size(640, 480));
VideoWriter blobRecord("recordedBlobs.mpeg", CV_FOURCC('P', 'I', 'M', '1'), 30, Size(640, 480));
int thresh[num_obj * 6];

string convertInt(int number) {
   stringstream ss;
   ss << number;
   return ss.str();
}

int setup() {
	load_thresh();
	init_opencv();
	return 0;
}

void load_thresh() {
	string line;
	ifstream myfile("vision/color.cfg");
	if (myfile.is_open()) {
		int obj_count = 0;
    	while (myfile.good()) {
    		for (int i = 0; i < 6; i++) {
      			getline(myfile, line);
      			if (line == "") {
      				break;
      			}
      			thresh[obj_count*6 + i] = atoi(line.c_str());
      			cout << thresh[obj_count*6 + i] << " ";
      		}
      		cout << endl;
      		if (line == "") {
      			break;
      		}
      		obj_count++;
    	}
    	myfile.close();
  	} else {
  		cout << "Unable to open file";
  	}
}
  	
int init_opencv() {
	if(!cap.isOpened())  // check if we succeeded
        return -1;
    
    // to initialize colors to the right size:
    cap >> src;
    colors.create(src.size(), CV_8U);
    resize(colors, colors, Size(), downsample_factor, downsample_factor, INTER_NEAREST);
    
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
    
    return 0;
} 

int step(Mat **frame_ptr, Mat **blob_ptr, Mat **scatter_ptr, int *thr, int num_colors) {

  bool force = true;
	if (num_colors == 0) {
		num_colors = num_obj;
		thr = thresh;
		force = false;
	}
	
    cap >> src; // get a new frame from camera
    //return 0;
    resize(src, ds, Size(), downsample_factor, downsample_factor, INTER_NEAREST);
    cvtColor(ds, hsv, CV_BGR2HSV);

    colors.setTo(Scalar(0));
    
    int numDetections = 0;
    for (int i = 0; i < maxDetections; i++) {
        objTypes[i] = "";
        objXCoords[i] = 0;
        objYCoords[i] = 0;
        objSizes[i] = 0;
    }
    for (int i = 0; i < num_colors; i++) {
        if (!obj_toggle[i] && !force) {
            continue;
        }
        if (numDetections >= maxDetections) {
            break;
        }
        int *t = &(thr[i * 6]);
        //cout << t[0] << " " << t[1] << endl;
        if (t[0] >= 0) {
            inRange(hsv, Scalar(t[0], t[2], t[4]), Scalar(t[1], t[3], t[5]), bw[i]);
        } else {
            int t_0 = 180 + t[0];
            inRange(hsv, Scalar(t_0, t[2], t[4]), Scalar(180, t[3], t[5]), bw[i]);
            inRange(hsv, Scalar(0, t[2], t[4]), Scalar(t[1], t[3], t[5]), temp);
            bitwise_or(bw[i], temp, bw[i]);
        }
        bitwise_or(colors, bw[i], colors);
        
        //cout << "detecting blobs:" << endl;
        blob_detector->detect(bw[i], keyPoints);
        //cout << keyPoints.size() << endl;
        
        
        for (int j = 0; j < keyPoints.size(); j++) {
            double scale = 1/downsample_factor;
            objTypes[numDetections] = obj[i];
            objXCoords[numDetections] = keyPoints[j].pt.x * scale;
            objYCoords[numDetections] = keyPoints[j].pt.y * scale;
            objSizes[numDetections] = keyPoints[j].size;
            numDetections++;
            if (numDetections == maxDetections) {
                break;
            }
        }
        
    }
    
    //cout << objSizes[0] << " " << objSizes[1] << " " << objSizes[2] << endl; 
    
    //erode(colors, colors, iterations=5);
    
    //morphologyEx(colors, colors, MORPH_CLOSE,
    //             getStructuringElement(MORPH_RECT, Size(3, 3)),
    //             Point(-1,-1), 5);
    
    //cout << objSizes[0] << " " << objSizes[1] << " " << objSizes[2] << endl;
    //drawKeypoints(colors, keyPoints, hsv, Scalar(0, 255, 0));
    
    
    //int out = 480 * (m.m10/m.m00) * scale + (m.m01/m.m00) * scale;
    int out = 0;
    //cout << keypoints << endl;
    //cout << endl;
    
    cvtColor(colors, colors3c, CV_GRAY2BGR);
    string frameCountStr = convertInt(frameCount);
    putText(colors3c, frameCountStr, cvPoint(5,15),
            FONT_HERSHEY_COMPLEX_SMALL, 0.8, Scalar(0,255,0));
    putText(src, frameCountStr, cvPoint(5,15),
            FONT_HERSHEY_COMPLEX_SMALL, 0.8, Scalar(0,255,0));
    
    if (frame_ptr != NULL) {
        *frame_ptr = &src;
    }
    if (blob_ptr != NULL) {
        *blob_ptr = &colors3c;
    }
    if (scatter_ptr != NULL) {
        *scatter_ptr = &colors;
    }
    
    rgbRecord << src;
    blobRecord << colors3c;
    
    frameCount++;
    
    return out;
}
