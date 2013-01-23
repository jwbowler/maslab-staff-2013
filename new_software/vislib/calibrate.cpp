#include "vision.h"

extern string *colorNames;
extern int numColors;
extern int **colorThresholds;
extern int *wallStripeThresholds;

extern Config cfg;

Mat *raw_display;
Mat *scatter_display;

int main() {

    setup();

	namedWindow("raw",1);
	namedWindow("blobs",1);
    
    for (int i = 0; i < numColors + 1; i++) {
        string s;
        int *t;
        Setting *colorInfoPtr;
        if (i != numColors) {
            s = colorNames[i];
            t = colorThresholds[i];
            Setting &colorsGroup = cfg.lookup("colors");
            colorInfoPtr = &(colorsGroup[i]);
        } else {
            s = "wall stripe";
            t = wallStripeThresholds;
            colorInfoPtr = &(cfg.lookup("wallStripeColor"));
        }
    	cout << "Calibrating " << s << endl;
    	for (int j = 0; j < 6; j++) {
    		cout << t[j] << " ";
    	}
    	cout << endl;

    	while (1) {
    	    
            if (i != numColors) {
    		    step(true, &raw_display, &scatter_display, i);
            } else {
                getWallImages(&raw_display, &scatter_display);
            }

    		imshow("raw", *raw_display);
            imshow("blobs", *scatter_display);
		    
        	char c = waitKey(1);
        	if (c == -1) {
        		continue;
        	}
        	if (c == ' ') {
                Setting &colorInfo = *colorInfoPtr;
                colorInfo["hueMin"] = t[0];
                colorInfo["hueMax"] = t[1];
                colorInfo["satMin"] = t[2];
                colorInfo["satMax"] = t[3];
                colorInfo["valMin"] = t[4];
                colorInfo["valMax"] = t[5];
                break;
        	}
        	switch (c) {
        		case 'q':
        			t[0] += 1;
        			break;
        		case 'a':
        			t[0] -= 1;
        			break;
        		case 'w':
        			t[1] += 1;
        			break;
        		case 's':
        			t[1] -= 1;
        			break;
        		case 'e':
        			t[2] += 1;
        			break;
        		case 'd':
        			t[2] -= 1;
        			break;
        		case 'r':
        			t[3] += 1;
        			break;
        		case 'f':
        			t[3] -= 1;
        			break;
        		case 't':
        			t[4] += 1;
        			break;
        		case 'g':
        			t[4] -= 1;
        			break;
        		case 'y':
        			t[5] += 1;
        			break;
        		case 'h':
        			t[5] -= 1;
        			break;
        			
        		case 'Q':
        			t[0] += 10;
        			break;
        		case 'A':
        			t[0] -= 10;
        			break;
        		case 'W':
        			t[1] += 10;
        			break;
        		case 'S':
        			t[1] -= 10;
        			break;
        		case 'E':
        			t[2] += 10;
        			break;
        		case 'D':
        			t[2] -= 10;
        			break;
        		case 'R':
        			t[3] += 10;
        			break;
        		case 'F':
        			t[3] -= 10;
        			break;
        		case 'T':
        			t[4] += 10;
        			break;
        		case 'G':
        			t[4] -= 10;
        			break;
        		case 'Y':
        			t[5] += 10;
        			break;
        		case 'H':
        			t[5] -= 10;
        			break;
        	}
        	for (int j = 0; j < 6; j++) {
        		cout << t[j] << " ";
        	}
        	cout << endl;
        	
    	}
    }
    cfg.writeFile("visionparams.cfg");    
}
