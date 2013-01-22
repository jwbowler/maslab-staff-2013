#ifndef _VISION_H
#define _VISION_H

#define CAMERA 1

#include "opencv2/opencv.hpp"
#include <libconfig.h++>
#include <iostream>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;
using namespace libconfig;

const double downsample_factor = .25;

const int maxDetections = 16;

int load_params();
int init_opencv();
int setup();
int step(bool isCalibMode = false, Mat **frame_ptr = NULL, Mat **scatter_ptr = NULL,
         int colorBeingCalibrated = 0);
int identify(Mat &image, Mat &colors, int *thresh, int num_colors);

#endif
