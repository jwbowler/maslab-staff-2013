#include <opencv2/opencv.hpp>
#include <ctime>

using namespace cv;
using namespace std;

int main() {

    VideoCapture cap(0);
    namedWindow("ds", 1);
    namedWindow("bw", 1);
    Mat src;
    Mat ds;
    Mat hsv;
    Mat bw;
    
    long double tLast = time(0);
    long double tAvg = 0;
    
    while (1) {
        cap >> src;
        if (src.empty())
            return -1;
            
        float scale = 0.5;
        resize(src, ds, Size(), scale, scale, INTER_NEAREST);

        cvtColor(ds, hsv, CV_BGR2HSV);

        inRange(hsv, Scalar(0, 130, 50), Scalar(10, 255, 245), bw);

        imshow("ds", ds);
        imshow("bw", bw);
        
        if (waitKey(10) != -1) {
			break;
		}
		
		long double tCurr = time(0);
		long double tDiff = tCurr - tLast;
		tLast = tCurr;
		tAvg = 0.9*tAvg + 0.1*tCurr;
		
		cout << 1000/tAvg << endl;
    }

    return 0;
}
