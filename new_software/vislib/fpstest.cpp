#include "vision.h"

VideoCapture cap(0);
Mat src;
int blah = 0;

int setup() {
    if (!cap.isOpened()) {
        return -1;
    }
}

int step() {
    cap >> src;
    cout << blah << endl;
    blah++;
}

int main() {
    setup();
    while (true) {
        step();
    }
}
