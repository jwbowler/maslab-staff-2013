from distutils.core import setup, Extension

module1 = Extension('vision',
                    libraries = ['opencv_core', 'opencv_highgui', 'opencv_imgproc', 'opencv_features2d'],
                    library_dirs = ['/usr/lib'],
                    sources = ['vision_module.cpp', 'vision.cpp'],
                    extra_compile_args = ['-O3'])

setup (name = 'vision',
       version = '1.0',
       description = 'Finds balls, and some other things.',
       ext_modules = [module1])
