#!/usr/bin/env python3

from setuptools import setup

setup(
    name='mir.qualia',
    version='0.2.0',
    description='Dynamically enable sections of config files.',
    long_description='',
    keywords='',
    url='https://github.com/darkfeline/mir.qualia',
    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
