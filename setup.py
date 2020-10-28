from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
import os


class CustomBuildExtCommand(build_ext):
    """build_ext command for use when numpy headers are needed."""
    def run(self):

        # Import numpy here, only when headers are needed
        import numpy

        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())

        # Call original build_ext command
        build_ext.run(self)

        
if os.name == 'nt':
    extra_compile_args = []
else:
    extra_compile_args = ['--std=c++11']

    
codingExt = Extension("_pyISCML",
                      sources=["cpp/pyISCML.i", "cpp/LdpcEncode.cpp", "cpp/MpDecode.cpp", "cpp/ConvEncode.cpp", "cpp/SisoDecode.cpp"],
                      define_macros=[('SWIG_PYTHON_INTERPRETER_NO_DEBUG', 1)],
                      language="c++",
                      swig_opts=['-c++', '-py3', '-modern', '-I../include' , '-DSMALL_LONG'],
                      extra_compile_args=extra_compile_args)

exts = [codingExt]

setup(name="pyISCML",
      cmdclass = {'build_ext': CustomBuildExtCommand},
      install_requires=['numpy'],
      ext_modules=exts,
      version = '0.1',
      description = """Python Bindings for Coded Modulation Library""")
