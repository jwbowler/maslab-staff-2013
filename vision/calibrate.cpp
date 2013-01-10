#include "balltracking.h"

Mat *raw_display;
Mat *scatter_display;
//Mat *hsv_display;

/*
static void onMouse(int event, int x, int y, int, void*) {
    cvtColor(*raw_display, *hsv_display, CV_BGR2HSV);
    cout << "HI" << endl;
}
*/

int main() {
    namedWindow("raw",1);
    namedWindow("scatter",1);
    
    //setMouseCallback("raw", onMouse, 0);
    
    Mat *raw_display;
    Mat *scatter_display;
    
    setup();
    
    run(&raw_display, &scatter_display);
    //*hsv_display = raw_display->clone();
    
    while (1) {
        int out = run(&raw_display, &scatter_display);
        cout << out/480 << " " << out%480 << endl;
        imshow("raw", *raw_display);
        imshow("scatter", *scatter_display);
        if (waitKey(10) > 0) {
            break;
        }
    }
}
