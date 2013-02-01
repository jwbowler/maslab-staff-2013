#ifndef _VISION_H
#define _VISION_H

#include "opencv2/opencv.hpp"
#include <libconfig.h++>
#include <iostream>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;
using namespace libconfig;

const int maxDetections = 8;

int load_params();
int init_opencv();
int setup();
int step(bool isCalibMode = false, Mat **frame_ptr = NULL, Mat **scatter_ptr = NULL,
         int colorBeingCalibrated = 0);
void updateWallMap();
void updateGoalMap();
void getWallImages(Mat **frame_ptr, Mat **scatter_ptr);
bool isBehindWall(int pixelX, int pixelY);
bool isInGoal(int pixelX, int pixelY);
void findBlobs(const cv::Mat &binaryImage, vector<Point2d> &centers, vector<Rect> &boxes, vector<int> &areas, vector<Point2d> &lowestPoint);

#endif
