from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "shamir_ss.shamir",
        ["shamir_ss/shamir.pyx"],
        extra_compile_args=["-O3", "-march=native"],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
        },
    )
)
