import os
import sys

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
        
    usage = "usage: %prog [options]\n Script to produce a list of ntuples"
        
    parser = OptionParser(usage)
    parser.add_option("-v","--version",default="Flatfish-v20190514",help="production version [default: %default]")
    parser.add_option("-p","--path",default="maite.iihe.ac.be/pnfs/iihe/cms/store/user/kskovpen/tHGG/Ntuple/",help="storage path [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options                                            

if __name__ == '__main__':
    
    options = main()

    fout = open("samples.xml","w+")
    fout.write('<data>\n')

    ntPath = options.path
    ntProd = options.version
    
    dlist = os.popen('gfal-ls srm://'+ntPath+ntProd+'/').read().splitlines()

    for i in dlist:
        print i
        isdata = str(int(i.find('DoubleEG') != -1))
        fout.write("    <sample id=\""+i+"\" isdata=\""+isdata+"\">\n")
        cpath = 'gfal-ls srm://'+ntPath+ntProd+'/'+i
        d1 = os.popen(cpath).read().splitlines()
        for i1 in d1:
            d2 = os.popen(cpath+'/'+i1).read().splitlines()
            if len(d2) != 1:
                print 'Several runs found in', i 
                exit
            for i2 in d2:
                d3 = os.popen(cpath+'/'+i1+'/'+i2).read().splitlines()
                for i3 in d3:
                    d3 = os.popen(cpath+'/'+i1+'/'+i2+'/'+i3).read().splitlines()
                    for i4 in d3:
                        fout.write("        <file>root://"+ntPath+ntProd+'/'+i+'/'+i1+'/'+i2+'/'+i3+'/'+i4+"</file>\n")
        fout.write("    </sample>\n")

    fout.write("</data>")

    fout.close()
