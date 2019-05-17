import os
import sys
import xml.etree.ElementTree as ET
import common as c

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
        
    usage = "usage: %prog [options]\n Script to produce a list of ntuples"
        
    parser = OptionParser(usage)
    parser.add_option("-n","--nfiles",default="30",help="number of files per job [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options                                            

if __name__ == '__main__':
    
    options = main()

    xmlTree = ET.parse(c.xmlName)
    for s in xmlTree.findall('sample'):
        for s0 in c.submit:
            if s.get('id') == s0:
                isdata = s.get('isdata')
                files=[]
                for child in s:
                    files.append(child.text)

                fout = open("job.xml","w+")
                fout.write('<data>\n')                
                fout.write("<sample id=\""+s0+"\" isdata=\""+isdata+"\">\n")
                for f in files:
                    fout.write("    <file>"+f+"</file>\n")
                fout.write("</sample>\n")                
                fout.write("</data>")
                fout.close()

                    
