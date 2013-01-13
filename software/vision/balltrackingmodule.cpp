#include <Python.h>
#include "balltracking.h"

#define BUILD_ARGS(x, y, z, w) x[0], y[0], z[0], w[0], x[1], y[1], z[1], w[1], \
                               x[2], y[2], z[2], w[2], x[3], y[3], z[3], w[3], \
                               x[4], y[4], z[4], w[4], x[5], y[5], z[5], w[5], \
                               x[6], y[6], z[6], w[6], x[7], y[7], z[7], w[7], \
                               x[8], y[8], z[8], w[8], x[9], y[9], z[9], w[9], \
                               x[10], y[10], z[10], w[10], x[11], y[11], z[11], w[11], \
                               x[12], y[12], z[12], w[12], x[13], y[13], z[13], w[13], \
                               x[14], y[14], z[14], w[14], x[15], y[15], z[15], w[15]

using namespace std;

string objTypes[16];
int visObjXCoords[16];
int objYCoords[16];
int objSizes[16];

static PyObject *balltracking_setup(PyObject *self, PyObject *args) {
    const char *command;
    int vec;

    if (!PyArg_ParseTuple(args, "", &command))
        return NULL;
    vec = setup();
    
    return Py_BuildValue("i", vec);
}

static PyObject *balltracking_step(PyObject *self, PyObject *args) {
    const char *command;
    int vec;

    if (!PyArg_ParseTuple(args, "", &command))
        return NULL;
    vec = step(NULL, NULL, NULL, NULL, 0);
    
    string format = "(siii)(siii)(siii)(siii)(siii)(siii)(siii)(siii)";
    
    /*
    cout << "HI" << endl;
    cout << objTypes[0].c_str() << " " << visObjXCoords[0] << " " << objYCoords[0] << " " << objSizes[0] << endl;
    cout << objTypes[1].c_str() << " " << visObjXCoords[1] << " " << objYCoords[1] << " " << objSizes[1] << endl;
    */
    return Py_BuildValue(format.c_str(),
        objTypes[0].c_str(), visObjXCoords[0], objYCoords[0], objSizes[0],
        objTypes[1].c_str(), visObjXCoords[1], objYCoords[1], objSizes[1],
        objTypes[2].c_str(), visObjXCoords[2], objYCoords[2], objSizes[2],
        objTypes[3].c_str(), visObjXCoords[3], objYCoords[3], objSizes[3],
        objTypes[4].c_str(), visObjXCoords[4], objYCoords[4], objSizes[4],
        objTypes[5].c_str(), visObjXCoords[5], objYCoords[5], objSizes[5],
        objTypes[6].c_str(), visObjXCoords[6], objYCoords[6], objSizes[6],
        objTypes[7].c_str(), visObjXCoords[7], objYCoords[7], objSizes[7]
        
        );
    
    //return Py_BuildValue(format.c_str(), "RED_BALL", 10, 10, 100, "YELLOW_WALL", 20, 20, 200);
}

static PyMethodDef BallTrackingMethods[] = {
    {"setup",  balltracking_setup, METH_VARARGS,
     "Setup openCV stuff."},
    {"step",  balltracking_step, METH_VARARGS,
     "Process one new camera frame."},
    {NULL, NULL, 0, NULL}      
};

PyMODINIT_FUNC initballtracking(void) {
    (void) Py_InitModule("balltracking", BallTrackingMethods);
}


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

/*
int main(int, char**) {
    setup();
    while (1) {
        run();
    }
    return 0;
}

int counts[640*480];
Mat frame;
Mat colors;
Mat hsv;
VideoCapture cap(0);

int setup() {
    //VideoCapture cap(1); // open camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    
    cap >> frame;
    colors = frame.clone();
    hsv = frame.clone();
    
    namedWindow("raw",1);
    namedWindow("scatter",1);

    int *j = counts;
    for (int i = 0; i < 640*480; i++) {
        *j = rand() % 1000;
        j++;
    }
    
    return 0;
}    

int run() {
    cap >> frame; // get a new frame from camera
    cvtColor(frame, hsv, CV_BGR2HSV);
        
    colors.setTo(Scalar(0));
      
    int out = identify(hsv, colors);
       
    imshow("raw", frame);
    imshow("scatter", colors);

    //cout << out << endl;
    
    return out;
}

int identify(Mat &image, Mat &colors) {

    int num_colors = 1;
    
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
        //cout << x << " " << y << " " << endl;
        //continue;
        
        char hue, sat, val;
        unsigned char *ptr;

        for (int i = 0; i < num_colors; i++) {
         	hue = input[image.step*y + 3*x];
         	sat = input[image.step*y + 3*x + 1];
         	val = input[image.step*y + 3*x + 2];
         	
         	
         	//cout << (int) hue << " " << (int) sat << " " << (int) val << endl;
        
            if ((hue >= 0 && hue < 10)
              && (sat > -114 && sat < 0)
              && (val > 50 || val < 0)) {
                //cout << "MATCH" << endl;
                output[colors.step*y + 3*x] = -1;
                output[colors.step*y + 3*x + 1] = -1;
                output[colors.step*y + 3*x + 2] = -1;
                addcount++;
                xsum += x;
                ysum += y;
            }
            
        }

    }
    
    if (addcount) {
        xsum /= addcount;
        ysum /= addcount;
        input[image.step*ysum + 3*xsum] = 127;
        input[image.step*ysum + 3*xsum + 1] = -1;
        input[image.step*ysum + 3*xsum + 2] = -1;
    }
    
    //cout << xsum << " " << ysum << endl;
    
    
    //if n < 2:
        //return (None, None)
    return xsum*480 + ysum;
    
}

*/

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
