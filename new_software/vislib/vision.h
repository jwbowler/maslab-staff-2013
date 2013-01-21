#ifndef _VISION_H
#define _VISION_H

#define CAMERA 1

#include "opencv2/opencv.hpp"
#include <iostream>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;

const string obj[] = {"RED_BALL", "GREEN_BALL", "YELLOW_WALL", "BLUE_WALL", "PURPLE_GOAL", "BLACK BUTTON"};
const bool obj_toggle[] = {true, true, false, false, false, false};
const int num_obj = 6;
const double downsample_factor = 0.25;

const int maxDetections = 16;

int setup();
void load_thresh();
int init_opencv();
int step(Mat **frame_ptr, Mat **hsv_ptr, Mat **scatter_ptr,
        int *thresh, int num_colors);
int identify(Mat &image, Mat &colors, int *thresh, int num_colors);

#endif
