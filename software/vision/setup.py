from distutils.core import setup, Extension

module1 = Extension('balltracking',
                    libraries = ['opencv_core', 'opencv_highgui', 'opencv_imgproc', 'opencv_features2d'],
                    library_dirs = ['/usr/lib'],
                    sources = ['balltrackingmodule.cpp', 'balltracking.cpp'])

setup (name = 'balltracking',
       version = '1.0',
       description = 'Tracks red balls.',
       ext_modules = [module1])
