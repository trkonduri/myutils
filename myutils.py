import os
import sys
import resource
import json
import subprocess
import pwd
import datetime


#print(os.path.realpath(__file__))


def list_files(basePath,validExts=None,contains=None):
    for rootDir, dirNames, fileNames in os.walk(basePath):
        for fileName in fileNames:
            if contains is not None and fileName.find(contains) == -1:
                continue
            # reverse find the "." from back wards
            ext = fileName[fileName.rfind("."):]
            if validExts is None or ext.endswith(validExts):
                file = os.path.realpath(os.path.join(rootDir,fileName))
                yield file

def mem_usage(tag):
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    denom = 1024
    if sys.platform == "darwin":
        denom = denom**2
    print(f'INFO: memory used is at {tag} : {round(mem/denom,2)} MB')

def beautify_json(file,outfile=None):
    js = json.loads(open(file).read())
    if outfile is None:
        outfile=file
    with open(outfile, 'w') as outfilep:
        json.dump(js,outfilep,sort_keys=True,indent=4)

def get_fuid(fileName):
    return(pwd.getpwuid(os.stat(fileName).st_uid).pw_name)

def execsh(command):
    result = subprocess.run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def mtimestamp(fileName):
    t = os.path.getmtime(fileName)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d-%H:%M")

def ctimestamp(fileName):
    t = os.path.getctime(fileName)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d-%H:%M")

if __name__ == "__main__":
    mem_usage("start")
    for a in list_files("./",(".py"), ("__init__")):
        print(a)
        print(get_fuid(a))
    print(mtimestamp("myutils.py"))
    print(ctimestamp("myutils.py"))

    mem_usage("end")





