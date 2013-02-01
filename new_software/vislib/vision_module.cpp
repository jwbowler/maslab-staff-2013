#include <Python.h>
#include "vision.h"

using namespace std;

extern string objTypes[16];
extern int objXCenters[16];
extern int objYCenters[16];
extern int objSizes[16];
extern int objXLowestPoints[16];
extern int objYLowestPoints[16];
extern bool objIsBehindWall[16];
extern bool objIsInGoal[16];
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
    
    string format = "i(siiiiiii)(siiiiiii)(siiiiiii)(siiiiiii)(siiiiiii)(siiiiiii)(siiiiiii)(siiiiiii)";
    
    /*
    cout << "HI" << endl;
    cout << objTypes[0].c_str() << " " << objXCoords[0] << " " << objYCoords[0] << " " << objSizes[0] << endl;
    cout << objTypes[1].c_str() << " " << objXCoords[1] << " " << objYCoords[1] << " " << objSizes[1] << endl;
    */
    return Py_BuildValue(format.c_str(), frameCount,
        objTypes[0].c_str(), objXCenters[0], objYCenters[0], objXLowestPoints[0], objYLowestPoints[0], objSizes[0], (int) objIsBehindWall[0], (int) objIsInGoal[0],
        objTypes[1].c_str(), objXCenters[1], objYCenters[1], objXLowestPoints[1], objYLowestPoints[1], objSizes[1], (int) objIsBehindWall[1], (int) objIsInGoal[1],
        objTypes[2].c_str(), objXCenters[2], objYCenters[2], objXLowestPoints[2], objYLowestPoints[2], objSizes[2], (int) objIsBehindWall[2], (int) objIsInGoal[2],
        objTypes[3].c_str(), objXCenters[3], objYCenters[3], objXLowestPoints[3], objYLowestPoints[3], objSizes[3], (int) objIsBehindWall[3], (int) objIsInGoal[3],
        objTypes[4].c_str(), objXCenters[4], objYCenters[4], objXLowestPoints[4], objYLowestPoints[4], objSizes[4], (int) objIsBehindWall[4], (int) objIsInGoal[4],
        objTypes[5].c_str(), objXCenters[5], objYCenters[5], objXLowestPoints[5], objYLowestPoints[5], objSizes[5], (int) objIsBehindWall[5], (int) objIsInGoal[5],
        objTypes[6].c_str(), objXCenters[6], objYCenters[6], objXLowestPoints[6], objYLowestPoints[6], objSizes[6], (int) objIsBehindWall[6], (int) objIsInGoal[6],
        objTypes[7].c_str(), objXCenters[7], objYCenters[7], objXLowestPoints[7], objYLowestPoints[7], objSizes[7], (int) objIsBehindWall[7], (int) objIsInGoal[7]
        
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
