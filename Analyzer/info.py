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
                for r, d, f in os.walk(options.dir+'/'+s0):
                    for file in f:
                        if '.root' in file:
                            inFile = ROOT.TFile.Open(options.dir+'/'+s+'/'+file,"OPEN")
                            counter = inFile.Get('counter')
                            inFile.Close()

                fout.write('    <sample xsec="'+str(xsec)+'">'+s+'</sample>\n')
                
        if not found:
            print 'Not found sample '+s
            exit

    fout.write('</data>\n')
    fout.close()
