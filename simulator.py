#this script will be the simulator for the testing of the UAS project

import sys
import os
import subprocess

def run_quadcopter(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out,err = proc.communicate()
    print('OUT: %s' % out)
    print('ERR: %s' % err)

def run_basestation(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out,err = proc.communicate()
    print('OUT: %s' % out)
    print('ERR: %s' % err)


if __name__ == "__main__":
    PYTHON_3 = 'C:\\Python33\\python.exe'
    PYTHON_2 = 'C:\\Python27\\python.exe'

    BASE_STATION_PATH = 'F:\\GitHub\\UAS\\elevation.py'
    MANAGER_PATH = 'F:\\GitHub\\UAS\\manager.py'

    if  not os.path.isfile(PYTHON_2) or not os.path.isfile(PYTHON_3):
        print("ERROR: Cannot find the Python programs")
        sys.exit(0)
    if not os.path.isfile(BASE_STATION_PATH) or not os.path.isfile(MANAGER_PATH):
        print("ERROR: Cannot find the scripts for base station and quadcopter")
        sys.exit(0)
    print("All needed files are present on the system")

    base_station_cmd = ("%s %s"%(PYTHON_3,BASE_STATION_PATH))
    quad_copter_cmd = ("%s %s"%(PYTHON_2,MANAGER_PATH))
    #both python programs are installed

    run_quadcopter(quad_copter_cmd)
    run_basestation(base_station_cmd)
        
