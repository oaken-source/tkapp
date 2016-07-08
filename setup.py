
from os.path import join, dirname
from setuptools import setup


setup(
    name='tkapp',
    version='0.0.0',

    description='a wrapper for tkinter that does stuff',
    long_description=open(join(dirname(__file__), 'README.md')).read(),

    packages=[
        'tkapp',
    ],

    install_requires=[],

    test_suite='tests',
    tests_require=[
        'pytest',
    ],

    setup_requires=['pytest_runner'],
)
