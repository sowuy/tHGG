import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import common as c

from optparse import OptionParser
try :
    from submit_slurm import submit_slurm
except ImportError:
    print "Slurm script not found"



def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    home = os.getcwd()

    usage = "usage: %prog [options]\n Script to submit Analyzer jobs to batch"

    parser = OptionParser(usage)
    parser.add_option("-f","--files",default="10",help="number of files per job [default: %default]")
    parser.add_option("-x","--xml",default="samples.xml",help="input xml configuration [default: %default]")
    parser.add_option("-p","--pdf",default=home+"/pdf.root",help="input file with pdfs [default: %default]")
    parser.add_option("-r","--run",default="",help="special run mode [default: %default]")
    parser.add_option("-t","--toprec",default=0,help="do top reconstruction [default: %default]")
    parser.add_option("-o","--out",default="jobs",help="output directory [default: %default]")
    parser.add_option("-n","--nmax",default="-1",help="number of processed events per job [default: %default]")
    parser.add_option("-b","--batch",default="slurm",help="batch system to use [default: %default]")

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
                fjobxml = []

                if os.path.isdir(outpath+"/"+s0):
                    os.system("rm -rf "+outpath+"/"+s0)
                os.system("mkdir "+outpath+"/"+s0)

                xml = outpath+"/"+s0+"/"+s0+"_"+str(nj)+".xml"
                fout = open(xml,"w+")
                fjobname.append(s0)
                fjobid.append(str(nj))
                fjobxml.append(xml)
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

                            xml = outpath+"/"+s0+"/"+s0+"_"+str(nj)+".xml"
                            fout = open(xml,"w+")
                            fjobname.append(s0)
                            fjobid.append(str(nj))
                            fjobxml.append(xml)
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

                    if (options.batch=='pbs'):
                        res = None
                        while res is None:
                            try:
                                res = subprocess.check_output(['qsub','-N','Analyzer','-q',c.batchqueue,'-o',outlog,'-j','oe','job.sh','-l','walltime='+c.walltime,'-v','nmax='+options.nmax+',sample='+f+',xml='+fjobxml[jid]+',output='+output+',dout='+home+',pdf='+options.pdf+',run='+options.run+',toprec='+str(options.toprec)+',proxy='+c.proxydir+c.proxy+',arch='+c.arch+' | grep -v \"Invalid credential\"'])
                            except KeyboardInterrupt:
                                sys.exit(0)
                            except:
                                pass
                    elif (options.batch=='slurm'):
                        submit_slurm(f,fjobxml[jid],output,nmax=options.nmax,pdf=options.pdf,run=options.run,toprec=options.toprec)
                    jid = jid + 1

