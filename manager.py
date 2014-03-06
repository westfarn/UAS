import subprocess
import time
import sys

if __name__ == '__main__':
    cmd_base = 'C:\Python27\python.exe F:\GitHub\UAS\opject_identification.py'
    filename_base = 'Pictures\\test_'
    #proc = False
    found_it = False
    picture_name = ''
    i = 0
    while not found_it and i < 12:
        i += 1
        filename = ("%s%i.jpg" % (filename_base,i))
        if i == 11:
            filename = 'Pictures/test2.jpg'
        #print(filename)
        cmd = ("%s %s" % (cmd_base,filename))
        #print(cmd)
        #proc = subprocess.call(cmd)
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        out,err = proc.communicate() # this is a blocking procedure
        print('OUT: %s' % out)
        print('ERR: %s' % err)
        #print(proc)
        if 'Return True' in out:
            found_it = True
            picture_name = filename
    if found_it:
        print("found the picture")
        sys.exit(1)
    else:
        print("didn't find the picture")
        sys.exit(0)

