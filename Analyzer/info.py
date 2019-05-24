import os
import sys
import subprocess
import common as c
import ROOT

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
        
    usage = "usage: %prog [options]\n Script to submit Analyzer jobs to batch"
        
    parser = OptionParser(usage)
    parser.add_option("-d","--dir",default="jobs",help="input directory with processed ntuples [default: %default]")
    parser.add_option("-o","--output",default="info.xml",help="output file name [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options                                            

if __name__ == '__main__':
    
    options = main()

    home = os.getcwd()    
    
    fout = open(options.output,"w+")
    fout.write('<data>\n')

    samples = next(os.walk(options.dir))[1]
    
    for s in samples:
        found = False
        for s0, xsec in c.submit:            
            if s0 == s:
                print s0
                found = True
                nEvents = 0
                files = []
                for r, d, f in os.walk(options.dir+'/'+s0):
                    for file in f:
                        if '.root' in file:
                            fname = options.dir+'/'+s+'/'+file
                            files.append(home+'/'+fname)
                            inFile = ROOT.TFile.Open(fname,"OPEN")
                            counter = inFile.Get('counter')
                            nEvents = nEvents + float(counter.GetBinContent(1))
                            inFile.Close()

                fout.write('    <sample id="'+s+'" '+'xsec="'+str(xsec)+'" '+'stat="'+str(nEvents)+'">\n')
                for f in files:
                    fout.write('        <file>'+f+'</file>\n')
                fout.write('    </sample>\n')
                    
                
        if not found:
            print 'Not found sample '+s
            exit

    fout.write('</data>\n')
    fout.close()
