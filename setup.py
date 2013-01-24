#!/usr/bin/env python
from setuptools import setup



setup(
    name='ircbot',
    version='0.1',
    packages=['ircbot'],
    url='http://casadirocco.nl/',
    author='Nico Di Rocco',
    author_email='dirocco.nico@gmail.com',
    description="A simple and minimal framework to create"\
                "bots for the irc network.",
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Chat :: Internet Relay Chat'
    ],
)
