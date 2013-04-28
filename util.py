import os.path

def Basename(path):
    return os.path.basename(os.path.splitext(path)[0])
