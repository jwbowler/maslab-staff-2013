#include "balltracking.h"

Mat *raw_display;
<<<<<<< HEAD
Mat *hsv_display;
Mat *scatter_display;

int test_thresh[num_obj * 6];
=======
Mat *scatter_display;
//Mat *hsv_display;

/*
static void onMouse(int event, int x, int y, int, void*) {
    cvtColor(*raw_display, *hsv_display, CV_BGR2HSV);
    cout << "HI" << endl;
}
*/
>>>>>>> 6a0e4712b81a62d4863b110dca893cff6a30f6c5

int main() {

	string line;
	ifstream tfile("color.cfg");
	if (tfile.is_open()) {
		int obj_count = 0;
    	while (tfile.good()) {
    		for (int i = 0; i < 6; i++) {
      			getline(tfile, line);
      			if (line == "") {
      				break;
      			}
      			test_thresh[obj_count*6 + i] = atoi(line.c_str());
      			//cout << test_thresh[obj_count*6 + i];
      		}
      		if (line == "") {
      			break;
      		}
      		cout << endl;
      		obj_count++;
    	}
    	tfile.close();
  	} else {
  		cout << "Unable to open file";
  	}
  	
    init_opencv();
		
	ofstream myfile("color.cfg");
	if (!myfile.is_open()) {
		cout << "failed to open file";
		return -1;
	}
	namedWindow("raw",1);
    namedWindow("scatter",1);
    
<<<<<<< HEAD
    
    for (int i = 0; i < num_obj; i++) {
    	string s = obj[i];
    	cout << "Calibrating " << s << endl;
    	for (int j = 0; j < 6; j++) {
    		cout << test_thresh[i*6 + j] << " ";
    	}
    	cout << endl;
    	while (1) {
    		run(&raw_display, &hsv_display, &scatter_display,
    		    &(test_thresh[i*6]), 1);
    		imshow("raw", *raw_display);
        	imshow("scatter", *scatter_display);
        	char c = waitKey(10);
        	if (c == -1) {
        		continue;
        	}
        	if (c == ' ') {
        		for (int j = 0; j < 6; j++) {
		    		myfile << test_thresh[i*6 + j] << endl;
		    	}
        		break;
        	}
        	switch (c) {
        		case 'q':
        			test_thresh[i*6 + 0] += 1;
        			break;
        		case 'a':
        			test_thresh[i*6 + 0] -= 1;
        			break;
        		case 'w':
        			test_thresh[i*6 + 1] += 1;
        			break;
        		case 's':
        			test_thresh[i*6 + 1] -= 1;
        			break;
        		case 'e':
        			test_thresh[i*6 + 2] += 1;
        			break;
        		case 'd':
        			test_thresh[i*6 + 2] -= 1;
        			break;
        		case 'r':
        			test_thresh[i*6 + 3] += 1;
        			break;
        		case 'f':
        			test_thresh[i*6 + 3] -= 1;
        			break;
        		case 't':
        			test_thresh[i*6 + 4] += 1;
        			break;
        		case 'g':
        			test_thresh[i*6 + 4] -= 1;
        			break;
        		case 'y':
        			test_thresh[i*6 + 5] += 1;
        			break;
        		case 'h':
        			test_thresh[i*6 + 5] -= 1;
        			break;
        			
        		case 'Q':
        			test_thresh[i*6 + 0] += 10;
        			break;
        		case 'A':
        			test_thresh[i*6 + 0] -= 10;
        			break;
        		case 'W':
        			test_thresh[i*6 + 1] += 10;
        			break;
        		case 'S':
        			test_thresh[i*6 + 1] -= 10;
        			break;
        		case 'E':
        			test_thresh[i*6 + 2] += 10;
        			break;
        		case 'D':
        			test_thresh[i*6 + 2] -= 10;
        			break;
        		case 'R':
        			test_thresh[i*6 + 3] += 10;
        			break;
        		case 'F':
        			test_thresh[i*6 + 3] -= 10;
        			break;
        		case 'T':
        			test_thresh[i*6 + 4] += 10;
        			break;
        		case 'G':
        			test_thresh[i*6 + 4] -= 10;
        			break;
        		case 'Y':
        			test_thresh[i*6 + 5] += 10;
        			break;
        		case 'H':
        			test_thresh[i*6 + 5] -= 10;
        			break;
        	}
        	for (int j = 0; j < 6; j++) {
        		cout << test_thresh[i*6 + j] << " ";
        	}
        	cout << endl;
    	}
=======
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
>>>>>>> 6a0e4712b81a62d4863b110dca893cff6a30f6c5
    }
    
    myfile.close();
}
