import os
import tempfile
import shutil
import json
import subprocess
import os
import multiprocessing
    #print (plot)

    #print (stdout.decode ().split('\n'))
    #print (stdout.decode ())

def justPrint  (tmpdir,stdout):
    print (stdout)
    
class Uppaal:
    def __init__ (self,uppaalinst,xmlpath, workqueuesize = 5):
        self._uppaalpath = os.path.abspath (uppaalinst)
        self._xmlpath = os.path.abspath (xmlpath)
        self._pool = multiprocessing.Pool (workqueuesize)

    def __setupDirectory (self,tmpdir):
        modelexec = os.path.join (tmpdir,"model.xml")
        shutil.copy (self._xmlpath,modelexec)
        return modelexec
                    

            
    def runHyperVerification (self,query,postprocess = None,discretisation = 1.0):
        pp = postprocess or parseEstim
        with tempfile.TemporaryDirectory() as tmpdir:

            querypath = os.path.join (tmpdir,"queery.q")
            with open (querypath,'w') as ff:
                ff.write (query)
            
            modelpath = self.__setupDirectory (tmpdir)
            binarypath = os.path.join (self._uppaalpath,"bin","verifyta")
            params = [binarypath,"-s","-q","--hyper.discretisation", str(discretisation), modelpath,querypath]
            res = subprocess.run (params,cwd = tmpdir,capture_output=True)
            return pp (tmpdir,res.stdout)
        
        
