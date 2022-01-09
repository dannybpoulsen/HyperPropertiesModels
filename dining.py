import hyper.uppaal
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

ALPHA = 0.01
EPSILON = 0.05


def equation_9 (locator,reslocator):
    reslocator = reslocator.makeSubLocator ("equation_9")
    modelpath = locator.findModel ("dining")
    all_done = "&&".join ([f"Cryptographer({i}).Done" for i in range(0,4)])
    uppaal = hyper.uppaal.Uppaal (locator.findUppaal (),modelpath)

    fig = plt.figure ()
    ax = fig.subplots ()
    for i in range (0,5):
        
        query = f"Pr[<=100] (<> {all_done} && pay == {i})"
        res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,0.1,alpha=ALPHA,epsilon=EPSILON)
        hist = res.getHistogram ()
        if hist:
            counts,bins = hist.counts(),hist.bins ()
            label = f"Cryptographer {i}"
            if i == 4:
                label = "Company"
            X = np.array (bins[:-1])
            Y = np.cumsum ([c/res.getTotalRuns ()  for c in counts])
            X_Y_SPLINE = make_interp_spline(X, Y)

            _X = np.linspace (X.min (),X.max (),5000)
            _Y = X_Y_SPLINE (_X)
            
            ax.plot(_X, _Y ,  label = label)
    ax.set_xlabel ("time")
    ax.set_ylabel ("Probability")
    ax.legend ()
    fig.savefig (reslocator.makeFilePath (f"Probability_of_payment.png"))

def equation_9_cond (locator,reslocator):
    inp = "DIning Conditional {0} - {1}"
    with hyper.uppaal.Progresser () as progress:
        
        reslocator = reslocator.makeSubLocator ("equation_9_cond")
        modelpath = locator.findModel ("dining")
        all_done = "&&".join ([f"Cryptographer({i}).Done" for i in range(0,4)])
        uppaal = hyper.uppaal.Uppaal (locator.findUppaal (),modelpath)

        fig = plt.figure ()
        ax = fig.subplots ()
        for i in range (0,5):
            x = []
            y = []
            for time in range(40,100,10):
                progress.message (inp.format (i,time))
                query = f"Pr {{1}} ((<>[0,{time}] pay == {i}) @ (<>[0,{time}] {all_done}) )"
                res = uppaal.runHyperVerification (query,hyper.uppaal.parseEstim,0.1,alpha=ALPHA,epsilon=EPSILON)
                prob  = res.getProbability ()
                x.append (time)
                y.append ((prob[0]+prob[1])/2)
            X = np.array (x)
            Y = np.array (y)
            X_Y_SPLINE = make_interp_spline(X, Y)

            _X = np.linspace (X.min (),X.max (),5000)
            _Y = X_Y_SPLINE (_X)
            label = f"Cryptographer {i}"
            if  i == 4:
                label = "Company"
            ax.plot(_X, _Y ,  label = label)
        ax.set_xlabel ("time")
        ax.set_ylabel ("Probability")
        ax.legend ()
        fig.savefig (reslocator.makeFilePath (f"Probability_of_paying.png"))




    
def dining_cryptographers (locator,reslocator):
    sublocator = reslocator.makeSubLocator ("dining_cryptographers")
    equation_9 (locator,sublocator)
    equation_9_cond (locator,sublocator)

    
