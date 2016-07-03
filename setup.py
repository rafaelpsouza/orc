from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='orc',
    version='1.0.0',
    description='ORC: Ops Remote Config. Put your tools configuration files in a remote git repository',
    long_description=long_description,
    url='https://github.com/rafaelpsouza/orc',
    author='Rafael de Paula Souza   ',
    author_email='rafaelpsouza.eng@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='devops development collectd sensu haproxy operation',
    
    packages=["orc"],

    install_requires=['schedule', 'gitpython'],

    entry_points = {
        "console_scripts": ['orc = orc.orc:main']
    },
)
