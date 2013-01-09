#ifndef _BALLTRACKING_H
#define _BALLTRACKING_H

#define CAMERA 1

#include "opencv2/opencv.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int setup();
int run(Mat **frame_ptr, Mat **scatter_ptr);
int identify(Mat &image, Mat &colors);

#endif
