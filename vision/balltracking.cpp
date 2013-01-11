#include "balltracking.h"

#define MIN3(x,y,z)  ((y) <= (z) ? \
                         ((x) <= (y) ? (x) : (y)) \
                     : \
                         ((x) <= (z) ? (x) : (z)))

#define MAX3(x,y,z)  ((y) >= (z) ? \
                         ((x) >= (y) ? (x) : (y)) \
                     : \
                         ((x) >= (z) ? (x) : (z)))

int getHue(int r, int g, int b);
int getSat(int r, int g, int b);
int getVal(int r, int g, int b);

/*
int getI(char r, char g, char b);
int getV(char r, char g, char b);
int getHPrime(char r, char g, char b);
int getHSI(char r, char g, char b);

int getHSV(char r, char g, char b) {
  i = r + b + g;

  max = 0;
  min = 0;
  c = 0;

  h = 0;
  s = 0;
  v = 0;

  if (r > g) {
    if (r > b) {
      max = r;
      if (b > g) {
        min = g;
      } else {
        min = b;
      }

      c = max - min;
      h = ((((g-b)<<8)/c) >> 8)

    } else {
      max = b;
      min = g;

      c = max-min;
      r-g/c

    }
  } else if (g > b) {
    max = g;
    if (r > b) {
      min = b;
    } else {
      min = r;
    }
    
    c = max-min;
    b-r/c

  } else {
    max = b;
    min = g;

    c = max-min;
  }

}

int getIPrime(char r, char g, char b) {
  return (r + g + b)
}

char getV(char r, char g, char b) {
  if (r > g) {
    if (r > b)
      return r;
    return b
  }
  if (g > b)
    return g;
  return b
}

int getHPrime(char r, char g, char b);
*/

int counts[640*480];
Mat frame;
Mat colors;
Mat hsv;
VideoCapture cap(CAMERA);
int thresh[num_obj * 6];

int setup() {
	load_thresh();
	init_opencv();
	return 0;
}

void load_thresh() {
	string line;
	ifstream myfile("vision/color.cfg");
	if (myfile.is_open()) {
		int obj_count = 0;
    	while (myfile.good()) {
    		for (int i = 0; i < 6; i++) {
      			getline(myfile, line);
      			if (line == "") {
      				break;
      			}
      			thresh[obj_count*6 + i] = atoi(line.c_str());
      			cout << thresh[obj_count*6 + i] << endl;
      		}
      		if (line == "") {
      			break;
      		}
      		obj_count++;
    	}
    	myfile.close();
  	} else {
  		cout << "Unable to open file";
  	}
}

int init_opencv() {
	if(!cap.isOpened())  // check if we succeeded
        return -1;
    
    cap >> frame;
    colors = frame.clone();
    hsv = frame.clone();

    int *j = counts;
    for (int i = 0; i < 640*480; i++) {
        *j = rand() % 1000;
        j++;
    }
    
    return 0;
} 

int step(Mat **frame_ptr, Mat **hsv_ptr, Mat **scatter_ptr, int *thr, int num_colors) {

	if (num_colors == 0) {
		num_colors = num_obj;
		thr = thresh;
	}
	
    cap >> frame; // get a new frame from camera
        
    colors.setTo(Scalar(0));
      
    int out = identify(frame, colors, thr, num_colors);
    
    if (frame_ptr != NULL) {
        *frame_ptr = &frame;
    }
    if (hsv_ptr != NULL) {
        *hsv_ptr = &hsv;
    }
    if (scatter_ptr != NULL) {
        *scatter_ptr = &colors;
    }
    
    return out;
}

int identify(Mat &image, Mat &colors, int *thresh, int num_colors) {
    
    //n = 0
    int *j = counts;
    
    int xsum = 0;
    int ysum = 0;
    int addcount = 0;
 	
	unsigned char *input = (unsigned char*) (image.data);
    unsigned char *output = (unsigned char*) (colors.data);
         	
    for (int c = 0; c < 640*480; c++) {
        //cout << j << endl;
        //cout << *j << endl;

        //(*j)++;
        //j++;
        
        counts[c]++;
        if (counts[c] & 0xFF) {
            continue;
        }
        
        int x = c / 480;
        int y = c % 480;
        
        /*
        char hue, sat, val;
        unsigned char *ptr;
        
     	hue = input[image.step*y + 3*x];
     	sat = input[image.step*y + 3*x + 1];
     	val = input[image.step*y + 3*x + 2];
     	
     	int h = (hue >= 0) ? hue : ((int) hue) + 256;
    	int s = (sat >= 0) ? sat : ((int) sat) + 256;
    	int v = (val >= 0) ? val : ((int) val) + 256;
    	*/
    	
    	char cr, cg, cb;
    	int r, g, b;
        unsigned char *ptr;
        
     	cb = input[image.step*y + 3*x];
     	cg = input[image.step*y + 3*x + 1];
     	cr = input[image.step*y + 3*x + 2];
     	
     	b = (cb >= 0) ? cb : ((int) cb) + 256;
    	g = (cg >= 0) ? cg : ((int) cg) + 256;
    	r = (cr >= 0) ? cr : ((int) cr) + 256;
     	
     	int h = getHue(r,g,b);
     	int s = getSat(r,g,b);
     	int v = getVal(r,g,b);

        for (int i = 0; i < num_colors; i++) {
        
        	if (!obj_toggle[i]) {
        		continue;
        	}
        	
        	int *t = &(thresh[i * 6]);
        	/*
        	cout << t[0] << " " << t[1] << " "
        	     << t[2] << " " << t[3] << " "
        	     << t[4] << " " << t[5] << endl;
        	     */
        	     
            if  ((h >= t[0] && h < t[1])
              && (s >= t[2] && s < t[3])
              && (v >= t[4] && v < t[5])) {
                output[colors.step*y + 3*x] = -1;
                output[colors.step*y + 3*x + 1] = -1;
                output[colors.step*y + 3*x + 2] = -1;
                addcount++;
                xsum += x;
                ysum += y;
            } else {
            	output[colors.step*y + 3*x] = -1;
                output[colors.step*y + 3*x + 1] = 127;
                output[colors.step*y + 3*x + 2] = 0;
            }
            
        }

    }
    
    if (addcount) {
        xsum /= addcount;
        ysum /= addcount;
        input[image.step*ysum + 3*xsum] = -1;
        input[image.step*ysum + 3*xsum + 1] = -1;
        input[image.step*ysum + 3*xsum + 2] = -1;
    }
    
    //cout << xsum << " " << ysum << endl;
    
    
    //if n < 2:
        //return (None, None)
    return xsum*480 + ysum;
    
    /*
    
    t = 30
    data = data[0:n, :]
    clusters = hcluster.fclusterdata(data, t, criterion="distance")
    
    return (data, clusters)
    */
}

/*
rgbToHsv(r, g, b){
    r = r/255, g = g/255, b = b/255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, v = max;

    var d = max - min;
    s = max == 0 ? 0 : d / max;

    if(max == min){
        h = 0; // achromatic
    }else{
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return [h, s, v];
}
*/

int getHue(int r, int g, int b) {
    int hue = 0;
    int base = 0;
    if (r >= g && r >= b) {
        base = 0;
        if (g > b) {
            if (r == b) {
                hue = 150;
            } else {
                hue = base + 30 * (g-b) / (r-b);
            }
        } else {
            if (r == g) {
                hue = 30;
            } else {
                hue = base - 30 * (b-g) / (r-g);
            }
        }
    } else if (g >= r && g >= b) {
        base = 60;
        if (b > r) {
            if (g == r) {
                hue = 30;
            } else {
                hue = base + 30 * (b-r) / (g-r);
            }
        } else {
            if (g == b) {
                hue = 90;
            } else {
                hue = base - 30 * (r-b) / (g-b);
            }
        }
    } else {
        base = 120;
        if (r > g) {
            if (b == g) {
                hue = 90;
            } else {
                hue = base + 30 * (r-g) / (b-g);
            }
        } else {
            if (b == r) {
                hue = 150;
            } else {
                hue = base - 30 * (g-r) / (b-r);
            }
        }
    }
    //cout << "hue:" << endl;
    //cout << hue << endl;
    return hue;
}

int getSat(int r, int g, int b) {
    //cout << "sat:" << endl;
    int out = MAX3(r, g, b) - MIN3(r, g, b);
    //cout << out << endl;
    return out;
}

int getVal(int r, int g, int b) {
    //cout << "val:" << endl;
    int out = MAX3(r, g, b);
    //cout << out << endl;
    return out;
}
