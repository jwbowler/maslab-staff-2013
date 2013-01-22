#include "vision.h"

extern string *colorNames;
extern bool *colorEnableFlags;
extern int numColors;
extern int **colorThresholds;

extern Config cfg;

Mat *raw_display;
Mat *hsv_display;
Mat *scatter_display;

//int colorThresholds[num_obj * 6];

int main() {

    /*
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
      			colorThresholds[obj_count*6 + i] = atoi(line.c_str());
      			cout << colorThresholds[obj_count*6 + i] << " ";
      		}
      		cout << endl;
      		if (line == "") {
      			break;
      		}
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
    */
    load_params();
    init_opencv();

    

	namedWindow("raw",1);
	namedWindow("blobs",1);
    //namedWindow("scatter",1);
    
    for (int i = 0; i < numColors; i++) {
    	string s = colorNames[i];
    	cout << "Calibrating " << s << endl;
    	for (int j = 0; j < 6; j++) {
    		cout << colorThresholds[i][j] << " ";
    	}
    	cout << endl;

    	while (1) {
    	    
    		int out = step(true, &raw_display, &scatter_display, i);

    		imshow("raw", *raw_display);
            imshow("blobs", *scatter_display);
		    
        	char c = waitKey(1);
        	if (c == -1) {
        		continue;
        	}
        	if (c == ' ') {
                //myfile << colorThresholds[i][j] << endl;

                Setting &colorsGroup = cfg.lookup("colors");
                Setting &colorInfo = colorsGroup[i];
                colorInfo["hueMin"] = colorThresholds[i][0];
                colorInfo["hueMax"] = colorThresholds[i][1];
                colorInfo["satMin"] = colorThresholds[i][2];
                colorInfo["satMax"] = colorThresholds[i][3];
                colorInfo["valMin"] = colorThresholds[i][4];
                colorInfo["valMax"] = colorThresholds[i][5];
                break;
        	}
        	switch (c) {
        		case 'q':
        			colorThresholds[i][0] += 1;
        			break;
        		case 'a':
        			colorThresholds[i][0] -= 1;
        			break;
        		case 'w':
        			colorThresholds[i][1] += 1;
        			break;
        		case 's':
        			colorThresholds[i][1] -= 1;
        			break;
        		case 'e':
        			colorThresholds[i][2] += 1;
        			break;
        		case 'd':
        			colorThresholds[i][2] -= 1;
        			break;
        		case 'r':
        			colorThresholds[i][3] += 1;
        			break;
        		case 'f':
        			colorThresholds[i][3] -= 1;
        			break;
        		case 't':
        			colorThresholds[i][4] += 1;
        			break;
        		case 'g':
        			colorThresholds[i][4] -= 1;
        			break;
        		case 'y':
        			colorThresholds[i][5] += 1;
        			break;
        		case 'h':
        			colorThresholds[i][5] -= 1;
        			break;
        			
        		case 'Q':
        			colorThresholds[i][0] += 10;
        			break;
        		case 'A':
        			colorThresholds[i][0] -= 10;
        			break;
        		case 'W':
        			colorThresholds[i][1] += 10;
        			break;
        		case 'S':
        			colorThresholds[i][1] -= 10;
        			break;
        		case 'E':
        			colorThresholds[i][2] += 10;
        			break;
        		case 'D':
        			colorThresholds[i][2] -= 10;
        			break;
        		case 'R':
        			colorThresholds[i][3] += 10;
        			break;
        		case 'F':
        			colorThresholds[i][3] -= 10;
        			break;
        		case 'T':
        			colorThresholds[i][4] += 10;
        			break;
        		case 'G':
        			colorThresholds[i][4] -= 10;
        			break;
        		case 'Y':
        			colorThresholds[i][5] += 10;
        			break;
        		case 'H':
        			colorThresholds[i][5] -= 10;
        			break;
        	}
        	for (int j = 0; j < 6; j++) {
        		cout << colorThresholds[i][j] << " ";
        	}
        	cout << endl;
        	
    	}
    }
    cfg.writeFile("visionparams.cfg");    
    //myfile.close();
}
