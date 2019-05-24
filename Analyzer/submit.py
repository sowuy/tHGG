import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import common as c

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
        
    usage = "usage: %prog [options]\n Script to submit Analyzer jobs to batch"
        
    parser = OptionParser(usage)
    parser.add_option("-f","--files",default="10",help="number of files per job [default: %default]")
    parser.add_option("-x","--xml",default="samples.xml",help="input xml configuration [default: %default]")
    parser.add_option("-o","--out",default="jobs",help="output directory [default: %default]")
    parser.add_option("-n","--nmax",default="-1",help="number of processed events per job [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options                                            

if __name__ == '__main__':
    
    options = main()
    
    os.system("cp /tmp/"+c.proxy+" "+c.proxydir+c.proxy)

    home = os.getcwd()    
    
    outpath = home+"/"+options.out
    
    if os.path.isdir(outpath):
        os.system("rm -rf "+outpath)

    os.system("mkdir "+outpath)
    
    xmlTree = ET.parse(options.xml)
    for s in xmlTree.findall('sample'):
        for s0, xsec in c.submit:
            if s.get('id') == s0:
                isdata = s.get('isdata')
                files=[]
                for child in s:
                    files.append(child.text)

                nj = 0
                fjobname = []
                fjobid = []
                
                if os.path.isdir(outpath+"/"+s0):
                    os.system("rm -rf "+outpath+"/"+s0)
                os.system("mkdir "+outpath+"/"+s0)

                xml = outpath+"/"+s0+"/"+s0+"_"+str(nj)+".xml"
                fout = open(xml,"w+")
                fjobname.append(s0)
                fjobid.append(str(nj))
                fout.write('<data>\n')                
                fout.write("<sample id=\""+s0+"\" isdata=\""+isdata+"\">\n")
                nc = 0
                for i in range(len(files)):
                    
                    nc = nc + 1
                    
                    fout.write("    <file>"+files[i]+"</file>\n")
                    
                    if (nc > int(options.files)):
                        fout.write("</sample>\n")
                        fout.write("</data>")
                        fout.close()

                        if (i != (len(files)-1)):
                            nc = 0
                            nj = nj + 1
                            
                            fout = open(xml,"w+")
                            fjobname.append(s0)
                            fjobid.append(str(nj))
                            fout.write('<data>\n')
                            fout.write("<sample id=\""+s0+"\" isdata=\""+isdata+"\">\n")

                if (nc <= int(options.files)):
                    fout.write("</sample>\n")
                    fout.write("</data>")
                    fout.close()

                jid = 0
                for f in fjobname:
                    
                    print f, fjobid[jid]
                    outname = outpath+'/'+f+'/'+f+'_'+fjobid[jid]
                    outlog = outname+'.log'
                    output = outname+'.root'
                    
                    while (str(subprocess.Popen(['qsub','-N','Analyzer','-q',c.batchqueue,'-o',outlog,'-j','oe','job.sh','-l','walltime='+c.walltime,'-v','nmax='+options.nmax+',sample='+f+',xml='+xml+',output='+output+',dout='+home+',proxy='+c.proxydir+c.proxy+',arch='+c.arch],stdout=subprocess.PIPE)).find('Invalid credential') != -1):
                        pass
                    
                    jid = jid + 1                    
