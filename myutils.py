import os
import sys
import resource

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

if __name__ == "__main__":
    mem_usage("start")
    for a in list_files("./",(".py"), ("__init__")):
        print(a)
    mem_usage("end")





