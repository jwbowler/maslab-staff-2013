#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main( int argc, char** argv )
{

    
    VideoCapture cap(0);
    Mat image;
    namedWindow( "Display window", CV_WINDOW_AUTOSIZE );
    
    while (1) {
        cap >> image;
        imshow( "Display window", image );                   // Show our image inside it.
        if (waitKey(10) > 0) {
            break;
        }
        
    }
    //waitKey(0);                                          // Wait for a keystroke in the window
    return 0;
}
