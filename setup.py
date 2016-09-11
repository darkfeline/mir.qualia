#!/usr/bin/env python3

from setuptools import setup

setup(
    name='mir.qualia',
    version='0.1.0',
    description='Enable sections of config files for different machines.',
    long_description='',
    keywords='',
    url='https://github.com/darkfeline/mir.qualia',
    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    license='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.5',
    ],

    packages=['mir.qualia'],
    entry_points={
        'console_scripts': [
            'qualia = mir.qualia.__main__:main',
        ],
    },
)
