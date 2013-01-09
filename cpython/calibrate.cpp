#include "balltracking.h"

int main() {
    namedWindow("raw",1);
    namedWindow("scatter",1);
    
    Mat *raw_display;
    Mat *scatter_display;
    
    //cout << "pre setup" << endl;
    setup();
    //cout << "post setup" << endl;
    
    while (1) {
        //cout << "pre run" << endl;
        int out = run(&raw_display, &scatter_display);
        cout << out << endl;
        //cout << "post run" << endl;
        imshow("raw", *raw_display);
        imshow("scatter", *scatter_display);
    }
}
