
import matplotlib
import matplotlib.pyplot as plt
import pyparsing as pp
import tempfile
import os
import sys
import numpy as np

import hyper.HPSTL
import hyper.uppaal

ALPHA = 0.01
EPSILON = 0.01
UPPER = 6
OBSDELTA = 0.1

def eventuallyAtom (atom,p,time):
    return hyper.HPSTL.Diamond (hyper.HPSTL.Atom (p,atom),0,time)


def atomAndEventuallyAtom (atom,p,q,time):
    return hyper.HPSTL.Conj (hyper.HPSTL.Atom(p,atom),eventuallyAtom (atom,q,time))



def makeOverallFormula(bound,delta):
    doneatom = "rsa.d"
    notdoneatom = "!rsa.d"

    leftconj = hyper.HPSTL.Conj (hyper.HPSTL.Atom (0,notdoneatom),hyper.HPSTL.Atom (1,notdoneatom))
    rightdisj = hyper.HPSTL.Disj (atomAndEventuallyAtom (doneatom,0,1,delta),atomAndEventuallyAtom (doneatom,1,0,delta))
    return f"Pr {{2}} ({hyper.HPSTL.Until (leftconj,rightdisj,0,bound)})"

def makeIterFormula(bound,delta,iterations = 8):
    conj = None
    for i in range (0,iterations):
        doneatom = f"rsa.iter_done[{i}]"
        notdoneatom = f"!{doneatom}"
    
        leftconj = hyper.HPSTL.Conj (hyper.HPSTL.Atom (0,notdoneatom),hyper.HPSTL.Atom (1,notdoneatom))
        rightdisj = hyper.HPSTL.Disj (atomAndEventuallyAtom (doneatom,0,1,delta),atomAndEventuallyAtom (doneatom,1,0,delta))
        nform = hyper.HPSTL.Until (leftconj,rightdisj,0,bound)
        if conj == None:
            conj = nform
        else:
            conj =hyper.HPSTL.Conj (nform,conj)

    return f"Pr {{2}} ({conj})"


def full_loop (locator,reslocator):
    inp = "RSA/FullLoop - {0} : {1}"
    with hyper.uppaal.Progresser () as progress:
        reslocator = reslocator.makeSubLocator ("full_loop")
        
        with open (locator.findModel ("rsa_sa"),'r') as ff:
            xmlcontent = ff.read ()

        
        with tempfile.TemporaryDirectory() as tmpdir:
            setup = {}
            probs = {}
            for label,conf in {"No Delay" : "NO_DELAY",
                            #   "Worst Case" : "WORST_CASE",
                               "Random Delay" : "RANDOM_DELAY"}.items ():
                path = os.path.join (tmpdir,f"{conf}.xml")
                with open (path,'w') as ff:
                    ff.write (xmlcontent.replace ("@ENABLE_RANDOM@",conf))
                setup[label] = hyper.uppaal.Uppaal (locator.findUppaal (),path)
            

            
            for i in range(1,UPPER):

                fig = plt.figure ()
                ax = fig.subplots ()
                query = makeOverallFormula(150,i)
                for l,uppaal in setup.items ():
                    progress.message (inp.format (i,l))
                    res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,OBSDELTA,alpha=ALPHA,epsilon=EPSILON)
                    hist = res.getHistogram ()
                    if hist:
                        counts,bins = hist.counts(),hist.bins ()
                        
                        ax.hist(bins[:-1], bins, weights=[c/res.getTotalRuns () for c in counts],histtype="step",label = f"{l}")
                    p = res.getProbability ()
                    probs[l] = probs.get(l,[])+[(p[0]+p[1])/2]
                ax.set_xlabel ("Satisfying Runs Run time")
                ax.set_ylabel ("Density")
                ax.legend (loc="right")
                fig.savefig (reslocator.makeFilePath (f"{i}.png"))

            nfig = plt.figure ()
            ax = nfig.subplots ()
            width = 1 / 3
            x = np.arange (UPPER-1)
            off = 0
            for l,ps in probs.items ():
                ax.bar(x+off, ps, width,label = l)
                off = off + width 
            ax.set_ylabel('Probability')
            ax.set_xticks(x, range(1,UPPER))
            ax.legend ()
            nfig.savefig (reslocator.makeFilePath ("probs.png"))
            
def iteration_property (locator,reslocator, iter = 8):
    inp = "RSA/Iteration - {0} : {1}"
    with hyper.uppaal.Progresser () as progress:
        reslocator = reslocator.makeSubLocator ("iteration")
        
        with open (locator.findModel ("rsa_sa"),'r') as ff:
            xmlcontent = ff.read ()


        with tempfile.TemporaryDirectory() as tmpdir:
            setup = {}
            probs = {}
            
            for label,conf in {"No Delay" : "NO_DELAY",
                            #   "Worst Case" : "WORST_CASE",
                               "Random Delay" : "RANDOM_DELAY"}.items ():
                path = os.path.join (tmpdir,f"{conf}.xml")
                with open (path,'w') as ff:
                    ff.write (xmlcontent.replace ("@ENABLE_RANDOM@",conf))
                    setup[label] = hyper.uppaal.Uppaal (locator.findUppaal (),path)


                    
            for i in range(1,UPPER):

                fig = plt.figure ()
                ax = fig.subplots ()
                query = makeIterFormula(150,i,iter)
                for l,uppaal in setup.items ():
                    progress.message (inp.format (i,l))
                    res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,OBSDELTA,alpha=ALPHA,epsilon=EPSILON)
                    hist = res.getHistogram ()
                    if hist:
                        counts,bins = hist.counts(),hist.bins ()
                        ax.hist(bins[:-1], bins, weights=[c/res.getTotalRuns () for c in counts],histtype="step",label = f"{l}")
                    p = res.getProbability ()
                    probs[l] = probs.get(l,[])+[(p[0]+p[1])/2]
                
                ax.set_xlabel ("Satisfying Runs Run time")
                ax.set_ylabel ("Density")
                ax.legend (loc="right")
                fig.savefig (reslocator.makeFilePath (f"{i}.png"))

            nfig = plt.figure ()
            ax = nfig.subplots ()
            width = 1.0 / 3
            x = np.arange (UPPER - 1)
            off = 0
            for l,ps in probs.items ():
                ax.bar(x+off, ps, width,label = l)
                off = off + width 
            ax.set_ylabel('Probability')
            ax.set_xticks(x, range(1,UPPER))
            ax.legend ()
               
            nfig.savefig (reslocator.makeFilePath ("probs.png"))
            

                
def rsa_example (locator,reslocator):
    sublocator = reslocator.makeSubLocator ("rsa")
    full_loop (locator,sublocator)
    iteration_property (locator,sublocator)
    

            


    
if __name__ == "__main__":
    import sys
    import os
    import tabulate
    #theHyperProperty ()
    theHyperIterProperty ()
    
    #plt.show ()
        
