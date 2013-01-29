#include <Python.h>
#include "vision.h"

#define BUILD_ARGS(x, y, z, w) x[0], y[0], z[0], w[0], x[1], y[1], z[1], w[1], \
                               x[2], y[2], z[2], w[2], x[3], y[3], z[3], w[3], \
                               x[4], y[4], z[4], w[4], x[5], y[5], z[5], w[5], \
                               x[6], y[6], z[6], w[6], x[7], y[7], z[7], w[7], \
                               x[8], y[8], z[8], w[8], x[9], y[9], z[9], w[9], \
                               x[10], y[10], z[10], w[10], x[11], y[11], z[11], w[11], \
                               x[12], y[12], z[12], w[12], x[13], y[13], z[13], w[13], \
                               x[14], y[14], z[14], w[14], x[15], y[15], z[15], w[15]

using namespace std;

extern string objTypes[16];
extern int objXCenters[16];
extern int objYCenters[16];
extern int objSizes[16];
extern int objXLowestPoints[16];
extern int objYLowestPoints[16];
extern bool objIsBehindWall[16];
extern int frameCount;

static PyObject *vision_setup(PyObject *self, PyObject *args) {
    const char *command;
    int vec;

    if (!PyArg_ParseTuple(args, "", &command))
        return NULL;
    vec = setup();
    
    return Py_BuildValue("i", vec);
}

static PyObject *vision_step(PyObject *self, PyObject *args) {
    const char *command;
    int vec;

    if (!PyArg_ParseTuple(args, "", &command))
        return NULL;
    vec = step();
    
    string format = "i(siiiiii)(siiiiii)(siiiiii)(siiiiii)(siiiiii)(siiiiii)(siiiiii)(siiiiii)";
    
    /*
    cout << "HI" << endl;
    cout << objTypes[0].c_str() << " " << objXCoords[0] << " " << objYCoords[0] << " " << objSizes[0] << endl;
    cout << objTypes[1].c_str() << " " << objXCoords[1] << " " << objYCoords[1] << " " << objSizes[1] << endl;
    */
    return Py_BuildValue(format.c_str(), frameCount,
        objTypes[0].c_str(), objXCenters[0], objYCenters[0], objXLowestPoints[0], objYLowestPoints[0], objSizes[0], (int) objIsBehindWall[0],
        objTypes[1].c_str(), objXCenters[1], objYCenters[1], objXLowestPoints[1], objYLowestPoints[1], objSizes[1], (int) objIsBehindWall[1],
        objTypes[2].c_str(), objXCenters[2], objYCenters[2], objXLowestPoints[2], objYLowestPoints[2], objSizes[2], (int) objIsBehindWall[2],
        objTypes[3].c_str(), objXCenters[3], objYCenters[3], objXLowestPoints[3], objYLowestPoints[3], objSizes[3], (int) objIsBehindWall[3],
        objTypes[4].c_str(), objXCenters[4], objYCenters[4], objXLowestPoints[4], objYLowestPoints[4], objSizes[4], (int) objIsBehindWall[4],
        objTypes[5].c_str(), objXCenters[5], objYCenters[5], objXLowestPoints[5], objYLowestPoints[5], objSizes[5], (int) objIsBehindWall[5],
        objTypes[6].c_str(), objXCenters[6], objYCenters[6], objXLowestPoints[6], objYLowestPoints[6], objSizes[6], (int) objIsBehindWall[6],
        objTypes[7].c_str(), objXCenters[7], objYCenters[7], objXLowestPoints[7], objYLowestPoints[7], objSizes[7], (int) objIsBehindWall[7]
        
        );
    
    //return Py_BuildValue(format.c_str(), "RED_BALL", 10, 10, 100, "YELLOW_WALL", 20, 20, 200);
}

static PyMethodDef VisionMethods[] = {
    {"setup",  vision_setup, METH_VARARGS,
     "Setup openCV stuff."},
    {"step",  vision_step, METH_VARARGS,
     "Process one new camera frame."},
    {NULL, NULL, 0, NULL}      
};

PyMODINIT_FUNC initvision(void) {
    (void) Py_InitModule("vision", VisionMethods);
}
