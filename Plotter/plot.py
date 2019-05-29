import os
import sys
import subprocess
import common as c
from subprocess import call
import xml.etree.ElementTree as ET
import math
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Analysis script to create histograms"
    
    parser = OptionParser(usage)
    parser.add_option("-n","--names",default="lepPt",help="list of histogram names [default: %default]")
    parser.add_option("-c","--channel",default="leptonic",help="analysis channel [default: %default]")
    parser.add_option("-o","--output",default="output.root",help="output file name [default: %default]")
    parser.add_option("-x","--xml",default="../Analyzer/info.xml",help="input xml configuration [default: %default]")
    parser.add_option("-b","--blind",default="1",help="blind analysis [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

if __name__ == '__main__':
    
    options = main()
                
    ROOT.gROOT.SetBatch()
    
    hnames = options.names.split(',')
    
    tree = {}
    
    xmlTree = ET.parse(options.xml)
    
    for p in c.process:
        tree[p] = {}
        for s1 in c.process[p]:
            for s2 in xmlTree.findall('sample'):                
                if s2.get('id') == s1:       
                    tr = ROOT.TChain(options.channel)
                    xsec = float(s2.get('xsec'))
                    stat = float(s2.get('stat'))
                    tree[p][s1] = [tr,xsec,stat]
                    for child in s2:
                        tree[p][s1][0].Add(child.text)

    hist = {}
    hinfo = {}
    for h in hnames:
        if options.channel == 'hadronic':
            if h == 'diPhoMass': hinfo['diPhoMass'] = [{'xtit':'Diphoton invariant mass [GeV]','nb':32,'xmin':100.,'xmax':180.,'ytit':'Events'}]
            elif h == 'diPhoMVA': hinfo['diPhoMVA'] = [{'xtit':'Diphoton MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
            elif h == 'phoLeadIDMVA': hinfo['phoLeadIDMVA'] = [{'xtit':'Leading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
            elif h == 'phoSubLeadIDMVA': hinfo['phoSubLeadIDMVA'] = [{'xtit':'Subleading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
        else:
            if h == 'diPhoMass': hinfo['diPhoMass'] = [{'xtit':'Diphoton invariant mass [GeV]','nb':7,'xmin':100.,'xmax':180.,'ytit':'Events'}]
            elif h == 'diPhoMVA': hinfo['diPhoMVA'] = [{'xtit':'Diphoton MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
            elif h == 'phoLeadIDMVA': hinfo['phoLeadIDMVA'] = [{'xtit':'Leading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
            elif h == 'phoSubLeadIDMVA': hinfo['phoSubLeadIDMVA'] = [{'xtit':'Subleading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]

    outFile = ROOT.TFile.Open(options.output,"RECREATE")
        
    for p in tree:
        hist[p] = {}
        for k, v in hinfo.iteritems():
            hname = 'h_'+k+'__'+p
            hist[p][k] = ROOT.TH1F(hname,hname,v[0]['nb'],v[0]['xmin'],v[0]['xmax'])
            hist[p][k].GetXaxis().SetTitle(v[0]["xtit"])
            hist[p][k].GetYaxis().SetTitle(v[0]["ytit"]) 
            hist[p][k].Sumw2()

    for p in tree:
        sys.stdout.write('Process '+p+':')
        for s in tree[p]:
            sys.stdout.write(' '+str(tree[p][s][0].GetEntries()))
            sys.stdout.flush()
            for ev in tree[p][s][0]:
                w = eval('ev.evWeight')
                wb = eval('ev.evWeightb')
                mgg = eval('ev.diPhoMass')
                phoLeadIDMVA = eval('ev.phoLeadIDMVA')
                phoSubLeadIDMVA = eval('ev.phoSubLeadIDMVA')
#                if phoLeadIDMVA < 0.8 or phoSubLeadIDMVA < 0.8: continue
#                if p in ['TTJets','TGJets','TTGJets']:
#                    w = wb
                if mgg < 100 or mgg > 180: continue
                if options.blind == '1' and p not in ['StHut','StHct','TtHut','TtHct']:
                    if mgg > 120 and mgg < 130:
                        continue
                if p != 'data': w = w * c.lumi / (tree[p][s][2]/tree[p][s][1])
                if math.fabs(w) > 10 and p in ['Others']: continue # manually remove large weight
                for k in hist[p]:
                    br = 'ev.'+k
                    v = eval(br)
                    hist[p][k].Fill(v,w)
        print ': \033[1;32mdone\033[1;m'

    outFile.Write()
    outFile.Close()
