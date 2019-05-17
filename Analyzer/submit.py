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
    parser.add_option("-o","--out",default="jobs",help="output directory [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options                                            

if __name__ == '__main__':
    
    options = main()    
    
    home = os.getcwd()
    
    outpath = home+"/"+options.out
    
    if os.path.isdir(outpath):
        os.system("rm -rf "+outpath)

    os.system("mkdir "+outpath)
    
    xmlTree = ET.parse(c.xmlName)
    for s in xmlTree.findall('sample'):
        for s0 in c.submit:
            if s.get('id') == s0:
                isdata = s.get('isdata')
                files=[]
                for child in s:
                    files.append(child.text)

                nj = 0
                fout = open(outpath+"/"+s0+"_"+str(nj)+".xml","w+")
                fout.write('<data>\n')                
                fout.write("<sample id=\""+s0+"\" isdata=\""+isdata+"\">\n")
                nc = 0
                for i in range(len(files)):
                    
                    nc = nc + 1
                    
                    if (nc > int(options.nfiles)):
                        fout.write("</sample>\n")
                        fout.write("</data>")
                        fout.close()
                        
                        nc = 0
                        nj = nj + 1
                        fout = open(outpath+"/"+s0+"_"+str(nj)+".xml","w+")
                        fout.write('<data>\n')
                        fout.write("<sample id=\""+s0+"\" isdata=\""+isdata+"\">\n")                        
                        
                    fout.write("    <file>"+files[i]+"</file>\n")
                    
                fout.write("</sample>\n")                
                fout.write("</data>")
                fout.close()

                    
