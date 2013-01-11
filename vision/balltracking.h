#ifndef _BALLTRACKING_H
#define _BALLTRACKING_H

#define CAMERA 1

#include "opencv2/opencv.hpp"
#include <iostream>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;

const string obj[] = {"RedBall", "GreenBall", "YellowWall", "BlueWall", "PurpleGoal"};
const bool obj_toggle[] = {true, true, false, false, false};
const int num_obj = 5;

int setup();
void load_thresh();
int init_opencv();
int step(Mat **frame_ptr, Mat **hsv_ptr, Mat **scatter_ptr,
        int *thresh, int num_colors);
int identify(Mat &image, Mat &colors, int *thresh, int num_colors);

#endif
