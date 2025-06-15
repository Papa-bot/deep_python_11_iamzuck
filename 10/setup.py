from setuptools import setup
from setuptools import Extension

ext = Extension(
    "custom_json",
    ["custom_json.c"],
    extra_compile_args=["-O3", "-Wall"],
)

setup(
    name="custom_json",
    version="0.1.0",
    ext_modules=[ext],
)
