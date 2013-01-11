#include <opencv2/opencv.hpp>
#include <ctime>

using namespace cv;
using namespace std;

int main() {

    VideoCapture cap(1);
    namedWindow("ds", 1);
    namedWindow("bw", 1);
    Mat src;
    Mat ds;
    Mat hsv;
    Mat bw;
    
    long double tLast = clock();
    long double tAvg = 0;
    
    int i = 0;
    while (1) {
        cap >> src;
        if (src.empty())
            return -1;
            
        tLast = clock();
            
        //float scale = 0.5;
        //resize(src, ds, Size(), scale, scale, INTER_NEAREST);
        
        
        cvtColor(src, hsv, CV_BGR2HSV);
        
        inRange(hsv, Scalar(0, 130, 50), Scalar(10, 255, 245), bw);
        
        Moments m = moments(bw, true);
        //cout << m.m10/m.m00 << " " << m.m01/m.m00 << endl;
        
        /*

        imshow("ds", src);
        imshow("bw", bw);
        
        if (waitKey(10) != -1) {
			break;
		}
		
		*/
		long double tCurr = clock();
		long double tDiff = tCurr - tLast;
		tLast = tCurr;
		tAvg = 0.9*tAvg + 0.1*tDiff;
		
		if (i%20 == 0) {
		    cout << CLOCKS_PER_SEC/tAvg << endl;
		}
		i++;
    }

    return 0;
}
