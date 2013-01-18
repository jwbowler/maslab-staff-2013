#include "vision.h"

int blah = 0;

int test_setup() {
    setup();
}

int test_step() {
    step(NULL, NULL, NULL, NULL, 0);
    cout << blah << endl;
    blah++;
}

int main() {
    test_setup();
    while (true) {
        test_step();
    }
}
