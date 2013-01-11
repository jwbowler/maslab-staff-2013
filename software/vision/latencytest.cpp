#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

int main() {
	VideoCapture cap(1);
	Mat frame;
	namedWindow("test",1);
	Mat buf1;
	Mat buf2;
	while (1) {
		cout << "1" << endl;
		/*
		while (1) {
			cout << "2" << endl;
			if (!cap.read(buf1)) {
				cout << "read 1" << endl;
				frame = &buf2;
				break;
			}
			if (!cap.read(buf2)) {
				cout << "read 2" << endl;
				frame = &buf1;
				break;
			}
		}
		*/
		cap >> frame;
		imshow("test", frame);
		if (waitKey(10) != -1) {
			break;
		}
	}
}
