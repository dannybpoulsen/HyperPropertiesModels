
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


def runAndMakeDensityPlot (modelpath,query,filepath):
    plt.clf ()
    plt.rcParams["figure.figsize"] = (5,2)
    uppaal =  hyper.uppaal.Uppaal (sys.argv[1],modelpath)
    res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,0.2,alpha = 0.01,epsilon = 0.01)
    
    hist = res.getHistogram () 
    bins,counts = hist.bins (), hist.counts ()
        
    plt.hist(bins[:-1], bins, weights=counts,density = True)
    
    plt.xlabel ("Run Duration")
    plt.ylabel ("Density")
    plt.savefig (filepath)
                    
    
def example3 (locator,resultlocator):
    inp = "Example 3 - {0}"
    with hyper.uppaal.Progresser () as progress:
        progress.message (inp.format ("failed"))
        modelpath = locator.findModel ("Login")
        respath  = resultlocator.makeSubLocator ("example3").makeFilePath ("login_failed.pdf")
        query = "Pr[<=10] (<> Process.signinfailed)"
        runAndMakeDensityPlot (modelpath,query,respath)

        progress.message (inp.format ("success"))
        modelpath = locator.findModel ("Login")
        respath  = resultlocator.makeSubLocator ("example3").makeFilePath ("login_succesful.pdf")
        query = "Pr[<=10] (<> Process.signinsuccess)"
        runAndMakeDensityPlot (modelpath,query,respath)

def example4 (locator,resultlocator):
    inp = "Example 4 - {0}"
    with hyper.uppaal.Progresser () as progress:
        modelpath = locator.findModel ("Login")
        reslocation = resultlocator.makeSubLocator ("example4")
        print ("Hyper Property")
        plt.clf ()
        plt.rcParams["figure.figsize"] = (5,2)

        tabledata = []
        for i in range(1,5):
            progress.message (inp.format (i))
            query = makeExample4Formula(100,i)
            uppaal =  hyper.uppaal.Uppaal (sys.argv[1],modelpath)
            res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,0.1,alpha=0.05,epsilon = 0.01)
            low,high = res.getProbability ()
            tabledata.append ([i,low,high,res.getConfidence ()])

            hist = res.getHistogram () 
            if hist:
                bins,counts = hist.bins (), hist.counts ()

                plt.hist(bins[:-1], bins, weights=[c / res.getTotalRuns () for c in counts],histtype="step",label = f"delta = {i}")

        plt.xlabel ("Satisfying Runs Runtime")
        plt.ylabel ("Density")
        plt.legend (loc="right")
        plt.savefig (reslocation.makeFilePath ("plot.pdf"))

        with reslocation.makeFile ("table.txt") as ff:
            ff.write (tabulate.tabulate (tabledata,headers =["delta","Low","High","Confidence"]))

def example5 (locator,resultlocator):
    inp = "Example 5 - {0}"
    with hyper.uppaal.Progresser () as progress:
        modelpath = locator.findModel ("Login")
        reslocation = resultlocator.makeSubLocator ("example5")
        uppaal =  hyper.uppaal.Uppaal (sys.argv[1],modelpath)

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

    locator = hyper.locator.Locator (".")
    sublocator = locator.makeSubLocator ("results")
    loginExamples (locator,sublocator)

    rsa.rsa_example (locator,sublocator)
        
