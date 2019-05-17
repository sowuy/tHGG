import os
import sys

ntProd = "Flatfish-v20190514"
ntPath = "maite.iihe.ac.be/pnfs/iihe/cms/store/user/kskovpen/tHGG/Ntuple/"

fout = open("samples.xml","w+")
fout.write('<data>\n')

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
