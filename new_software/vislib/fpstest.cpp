#include <iostream>
#include <unistd.h>
#include <sys/time.h>
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;

VideoCapture cap(1);
Mat src;
int blah = 0;
struct timeval startTime, endTime;
long seconds, useconds;
double mtime;

int setup() {
    if (!cap.isOpened()) {
        return -1;
    }
}

int step() {
    cap >> src;
    //cout << blah << endl;
    blah++;
}

int main() {
    setup();
    gettimeofday(&startTime, NULL);

    while (true) {
        step();
        usleep(10000);

        gettimeofday(&endTime, NULL);
        seconds = endTime.tv_sec - startTime.tv_sec;
        useconds = endTime.tv_usec - startTime.tv_usec;
        mtime = (seconds + useconds/1000000.);
        cout << 1./mtime << endl;
        startTime = endTime;
    }
}
