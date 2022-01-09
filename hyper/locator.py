import os
import errno

class UppaalNotFound(BaseException):
    def __init__ (self,path):
        self._path = path

    def __str__ (self):
        return f"Uppaal not found in {self._path}"

    def getPath (self):
        return self._path

class Locator:
    def __init__ (self,root = os.path.split (os.path.abspath (__file__))[0]):
        self._root = os.path.abspath (root)
        
    def findModel (self,name):
        path = os.path.join (self._root,"models",name+".xml")
        if os.path.exists (path):
            return path
        else:
            raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), path)

    def findUppaal (self):
        path = os.path.join (self._root,"bin")
        os.makedirs(path,exist_ok = True)
        for dirpath,dirnames,filenames in os.walk (path):
            for d in dirnames:
                if "uppaal" in d:
                    return os.path.join (dirpath,d)
        else:
            raise UppaalNotFound (path)


    def makeSubLocator (self,subdir):
        path = os.path.join (self._root,subdir)
        os.makedirs(path,exist_ok = True)
        return Locator (path)
        
    def makeFile (self,filename):
        return open (os.path.join (self._root,filename),'w')

    def makeFilePath (self,filename):
        return os.path.join (self._root,filename)

        
