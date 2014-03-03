import subprocess
import time


if __name__ == '__main__':
	cmd = 'C:\Python27\python.3x3 F:\GitHub\UAS\opject_identification.py'
	result = subprocess.call(cmd)
	while not result:
		result = subprocess.call(cmd)
		time.sleep(5)
	print("Found a circle")

