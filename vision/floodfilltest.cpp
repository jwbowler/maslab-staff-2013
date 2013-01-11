#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int main() {

    VideoCapture cap(0);
    namedWindow("ds", 1);
    namedWindow("bw", 1);
    Mat src;
    while (1) {
        cap >> src;
        if (src.empty())
            return -1;
            
        Mat ds;
        float scale = 0.5;
        resize(src, ds, Size(), scale, scale, INTER_NEAREST);

        Mat hsv;
        cvtColor(ds, hsv, CV_BGR2HSV);

        Mat bw;
        inRange(hsv, Scalar(0, 130, 50), Scalar(10, 255, 245), bw);

        imshow("ds", ds);
        imshow("bw", bw);
        
        if (waitKey(10) != -1) {
			break;
		}
    }

    return 0;
}
