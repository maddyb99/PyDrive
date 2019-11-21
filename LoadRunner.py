import sys
import os
from os import listdir
from os.path import isfile, join

def testPyDrive():
    onlyfiles = [f for f in listdir("./img/") if isfile(join("./img/", f))]
    arg=""
    # print(onlyfiles)
    for f in onlyfiles[1:2500]:
        # print(f)
        arg += './img/{} '.format(f)
        # arg=arg.join(" ./img/")
        # arg=arg.join(f)
    # print(arg)
    # os.system("python3 main.py "+arg+ " &")
    arg2=""
    for f in onlyfiles[2501:5000]:
        arg2 += './img/{} '.format(f)
    arg3=""
    for f in onlyfiles[5001:7500]:
        arg3 += './img/{} '.format(f)
    arg4=""
    for f in onlyfiles[7501:10000]:
        arg4 += './img/{} '.format(f)
    os.system("python3 main.py "+arg+ " & "+"python3 main.py "+arg2+ " & ")
    os.system("python3 main.py "+arg3+ " & "+"python3 main.py "+arg4+ " &")
    os.system("sleep 60")
    # os.system("sudo pkill python3")
    onlynewfiles = [f for f in listdir("./edge/") if isfile(join("./edge/", f))]
    flag=True
    for a, b in zip(onlyfiles[1:1000],onlynewfiles):
        if a!=b:
            flag=False
            break
    if(flag):
        print("Success")
    else:
        print("Failed")


def main():
    testPyDrive()

if __name__ == '__main__':
    main()