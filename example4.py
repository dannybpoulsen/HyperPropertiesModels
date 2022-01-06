
import matplotlib
import matplotlib.pyplot as plt
import pyparsing as pp

import hyper.HPSTL
import hyper.uppaal

def eventuallyAtom (atom,p,time):
    return hyper.HPSTL.Diamond (hyper.HPSTL.Atom (p,atom),0,time)


def atomAndEventuallyAtom (atom,p,q,time):
    return hyper.HPSTL.Conj (hyper.HPSTL.Atom(p,atom),eventuallyAtom (atom,q,time))



def makeFormula(bound,delta):
    doneatom = "Process.Done"
    notdoneatom = "!Process.Done"

    leftconj = hyper.HPSTL.Conj (hyper.HPSTL.Atom (0,notdoneatom),hyper.HPSTL.Atom (1,notdoneatom))
    rightdisj = hyper.HPSTL.Disj (atomAndEventuallyAtom (doneatom,0,1,delta),atomAndEventuallyAtom (doneatom,1,0,delta))
    return f"Pr {{2}} ({hyper.HPSTL.Until (leftconj,rightdisj,0,bound)})"



def parsePlot (line):
    interval = (pp.Literal ("[") + pp.pyparsing_common.number + pp.Literal (",") + pp.pyparsing_common.number + pp.Literal ("]")).setParseAction ( lambda s,l,t: (t[1],t[3]))
    valuesIN = (pp.Literal ("Values in") + interval).setParseAction (lambda s,l,t: t[1])
    mean = (pp.Literal ("mean=")+pp.pyparsing_common.number ()).setParseAction (lambda s,l,t: t[1])
    steps = (pp.Literal ("steps=")+pp.pyparsing_common.number ()).setParseAction (lambda s,l,t: t[1])
    values = (pp.Literal (":")+pp.OneOrMore (pp.pyparsing_common.number ())).setParseAction (lambda s,l,t: t[1:])
    parser = valuesIN+mean+steps+values
    res = parser.parseString (line)
    ran,mean,steps,counts = res[0],res[1],res[2],res[3:]
    print (ran)
    print (steps)
    return [(ran[0]+i*steps,ran[0]+(i+1)*steps,val) for i,val in enumerate (counts)]


def parseProb (line):
    parser = (pp.Literal ("Pr(Hyper) in [")+pp.pyparsing_common.number ()+pp.Literal (",")+pp.pyparsing_common.number ()+pp.Literal("] (")+pp.pyparsing_common.number()+pp.Literal("% CI)")).setParseAction (lambda s,l,t:
                                                                                                                                                                                                             (t[1],t[3],t[5]))
    return parser.parseString (line)[0]
    
    
def parseEstim (tmpdir,stdout):
    print (stdout)
    lines = stdout.decode().split('\n')
    resline = lines[2]
    print (resline)
    if "Formula is satisfied." in resline:
        probline = lines[3]
        plot = lines[5]
        return parsePlot (plot),parseProb (probline)


    
if __name__ == "__main__":
    import sys
    import os
    import tabulate
    tabledata = []
    for i in range(1,5):
        print (i)
        query = makeFormula(100,i)
        print (f"Query: {query}") 
        modelxml = os.path.join (os.path.split(os.path.abspath (__file__))[0],"models","Login.xml")
        uppaal =  hyper.uppaal.Uppaal (sys.argv[1],modelxml)
        histo,prob = uppaal.runHyperVerification (query,parseEstim,0.1)
        print (prob)
        tabledata.append ([i,prob[0],prob[1],prob[2]])
        
        
        counts = [t[2] for t in histo]
        bins = [t[0] for t in histo]+[histo[-1][1]]
        
        plt.hist(bins[:-1], bins, weights=counts,density = True,histtype="step",label = f"delta = {i}")
    
    plt.xlabel ("Satisfying Runs Run time")
    plt.ylabel ("Density")
    plt.legend (loc="right")
    os.makedirs ("example4",exist_ok =True)
    plt.savefig (os.path.join ("example4","example4.pdf"))

    with open(os.path.join ("example4","table,txt"),'w') as ff:
        ff.write (tabulate.tabulate (tabledata,headers =["delta","Low","High","Confidence"]))
    
    #plt.show ()
        
