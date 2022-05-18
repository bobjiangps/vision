from distutils.core import setup
from Cython.Build import cythonize
import numpy

# setup(
#     # ext_modules = cythonize("pyx_python.pyx")
#     ext_modules = cythonize("cy_python.py")
#     # ext_modules = cythonize("levenshtein.pyx")
# )

setup(
    ext_modules=cythonize("levenshtein.pyx"),
    include_dirs=[numpy.get_include()]
)