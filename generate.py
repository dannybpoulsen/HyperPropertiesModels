
import matplotlib

import matplotlib.pyplot as plt
import pyparsing as pp

import hyper.HPSTL
import hyper.uppaal

def eventuallyAtom (atom,p,time):
    return hyper.HPSTL.Diamond (hyper.HPSTL.Atom (p,atom),0,time)


def atomAndEventuallyAtom (atom,p,q,time):
    return hyper.HPSTL.Conj (hyper.HPSTL.Atom(p,atom),eventuallyAtom (atom,q,time))



def makeExample4Formula(bound,delta):
    doneatom = "Process.Done"
    notdoneatom = "!Process.Done"

    leftconj = hyper.HPSTL.Conj (hyper.HPSTL.Atom (0,notdoneatom),hyper.HPSTL.Atom (1,notdoneatom))
    rightdisj = hyper.HPSTL.Disj (atomAndEventuallyAtom (doneatom,0,1,delta),atomAndEventuallyAtom (doneatom,1,0,delta))
    return f"Pr {{2}} ({hyper.HPSTL.Until (leftconj,rightdisj,0,bound)})"


def runAndMakeDensityPlot (modelpath,query,filepath,upppath):
    fig = plt.figure ()
    ax = fig.subplots ()
    uppaal =  hyper.uppaal.Uppaal (upppath,modelpath)
    res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,0.2,alpha = 0.01,epsilon = 0.01)
    
    hist = res.getHistogram () 
    bins,counts = hist.bins (), hist.counts ()
        
    ax.hist(bins[:-1], bins, weights=counts,density = True)
    
    ax.set_xlabel ("Run Duration")
    ax.set_ylabel ("Density")
    fig.savefig (filepath)
                    
    
def example3 (locator,resultlocator):
    inp = "Example 3 - {0}"
    with hyper.uppaal.Progresser () as progress:
        progress.message (inp.format ("failed"))
        modelpath = locator.findModel ("Login")
        respath  = resultlocator.makeSubLocator ("example3").makeFilePath ("login_failed.pdf")
        query = "Pr[<=10] (<> Process.signinfailed)"
        runAndMakeDensityPlot (modelpath,query,respath,locator.findUppaal ())

        progress.message (inp.format ("success"))
        modelpath = locator.findModel ("Login")
        respath  = resultlocator.makeSubLocator ("example3").makeFilePath ("login_succesful.pdf")
        query = "Pr[<=10] (<> Process.signinsuccess)"
        runAndMakeDensityPlot (modelpath,query,respath,locator.findUppaal ())

def example4 (locator,resultlocator):
    inp = "Example 4 - {0}"
    with hyper.uppaal.Progresser () as progress:
        modelpath = locator.findModel ("Login")
        reslocation = resultlocator.makeSubLocator ("example4")
        print ("Hyper Property")
        fig = plt.figure ()
        ax = fig.subplots ()
        #plt.rcParams["figure.figsize"] = (5,2)

        tabledata = []
        for i in range(1,5):
            progress.message (inp.format (i))
            query = makeExample4Formula(100,i)
            uppaal =  hyper.uppaal.Uppaal (locator.findUppaal (),modelpath)
            res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,0.1,alpha=0.05,epsilon = 0.01)
            low,high = res.getProbability ()
            tabledata.append ([i,low,high,res.getConfidence ()])

            hist = res.getHistogram () 
            if hist:
                bins,counts = hist.bins (), hist.counts ()
            
                ax.hist(bins[:-1], bins, weights=[c / res.getTotalRuns () for c in counts],histtype="step",label = f"delta = {i}")

        ax.set_xlabel ("Satisfying Runs Runtime")
        ax.set_ylabel ("Density")
        ax.legend (loc="right")
        fig.savefig (reslocation.makeFilePath ("plot.pdf"))

        with reslocation.makeFile ("table.txt") as ff:
            ff.write (tabulate.tabulate (tabledata,headers =["delta","Low","High","Confidence"]))

def example5 (locator,resultlocator):
    inp = "Example 5 - {0}"
    with hyper.uppaal.Progresser () as progress:
        modelpath = locator.findModel ("Login")
        reslocation = resultlocator.makeSubLocator ("example5")
        uppaal =  hyper.uppaal.Uppaal (locator.findUppaal (),modelpath)

        tabledata = []
        for i in range (2,20):
            progress.message (inp.format (i))
            d = [i]
            for q in  [f"Pr {{1}} ((<>[0,{i}] Process.signinfailed) @ (<>[0,{i}] Process.Done))",
                       f"Pr {{1}} ((<>[0,{i}] Process.signinsuccess) @ (<>[0,{i}] Process.Done))"
                       ]:
                res = uppaal.runHyperVerification (q,hyper.uppaal.parseEstim,0.2,alpha  = 0.01, epsilon = 0.01)
                low,high = res.getProbability ()
                conf = res.getConfidence ()
                d+= [f"[{low},{high}]",str(conf)]
            tabledata.append(d)
        with reslocation.makeFile ("table.txt") as ff:
            ff.write (tabulate.tabulate (tabledata,headers =["delta","Pr (Fail | Done)","Confidence","Pr (Success | Done)","Confidence"]))

def loginExamples (locator,resloc):
    sublocator = resloc.makeSubLocator ("Login")
    example3 (locator,sublocator)
    example4 (locator,sublocator)
    example5 (locator,sublocator)
    

    
    
if __name__ == "__main__":
    import sys
    import os
    import tabulate
    import hyper.locator
    import rsa
    import dining

    locator = hyper.locator.Locator (".")
    sublocator = locator.makeSubLocator ("results")

    try:
        #try Uppaal  locating Uppaal installation
        path = locator.findUppaal ()
    except hyper.locator.UppaalNotFound as ex:
        path = ex.getPath ()
        print (f"Uppaal Not found at {path}")
        import urllib3
        import zipfile
        import io

        
    #Code from https://stackoverflow.com/questions/39296101/python-zipfile-removes-execute-permissions-from-binaries
        url = "http://localhost:8000/uppaal-DEV-stratego-hyper-linux64.zip"
        print (f"Downloading pre-release from: {url}")
        http = urllib3.PoolManager ()
        try:
            r = http.request ('GET',url)
        except urllib3.exceptions.MaxRetryError:
            print (f"Can't connect to {url}")
            exit ()
        if r.status == 200:
            zf = zipfile.ZipFile(io.BytesIO(r.data), "r")
            for info in zf.infolist  ():
                zf.extract (info.filename,path)
                outpath = os.path.join (path,info.filename)
                os.chmod (outpath, (info.external_attr >> 16))
        else:
            print (f"Error downloading Uppaal from {url}")
            exit ()



            
    loginExamples (locator,sublocator)
    rsa.rsa_example (locator,sublocator)
    dining.dining_cryptographers (locator,sublocator)
