import os
import sys
import subprocess
import common as c
from subprocess import call
import xml.etree.ElementTree as ET
from array import array
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
    parser.add_option("-s","--selection",default="",help="additional selection [default: %default]")

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

    sel = [""]
    if options.selection != "": sel.extend(options.selection.split(','))
    ncat = int(len(sel))

    isLep = bool(options.channel == 'leptonic')

    helep = [dict() for x in range(ncat)]
    hmlep = [dict() for x in range(ncat)]
    hlep = [dict() for x in range(ncat)]
    hhad = [dict() for x in range(ncat)]

    hist = {}
    hinfo = {}

    if not isLep:
        hinfo['All'] = hhad
    else:
        hinfo['All'] = hlep
        hinfo['Elec'] = helep
        hinfo['Muon'] = hmlep

    for h in hnames:
        if not isLep:
            for s, hd in enumerate(hhad):
                sstr = sel[s]
                if sstr != "": sstr = '_'+sstr
                if h == 'diPhoMass': hd['diPhoMass'+sstr] = [{'xtit':'Diphoton invariant mass [GeV]','nb':32,'xmin':100.,'xmax':180.,'ytit':'Events'}]
                elif h == 'diPhoMVA': hd['diPhoMVA'+sstr] = [{'xtit':'Diphoton MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
                elif h == 'phoLeadIDMVA': hd['phoLeadIDMVA'+sstr] = [{'xtit':'Leading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
                elif h == 'phoSubLeadIDMVA': hd['phoSubLeadIDMVA'+sstr] = [{'xtit':'Subleading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
                else:
                    continue
        else:
            for ch, hl in hinfo.items():
                cstr = ch
                cstr = '_'+cstr
                for s, hd in enumerate(hl):
                    sstr = sel[s]
                    if sstr != "": sstr = '_'+sstr
                    if h == 'diPhoMass': hd['diPhoMass'+cstr+sstr] = [{'xtit':'Diphoton invariant mass [GeV]','nb':8,'xmin':100.,'xmax':180.,'ytit':'Events'}]
                    elif h == 'diPhoMVA': hd['diPhoMVA'+cstr+sstr] = [{'xtit':'Diphoton MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
                    elif h == 'diPhoPt': hd['diPhoPt'+cstr+sstr] = [{'xtit':'Diphoton pT [GeV]','nb':30,'xmin':0,'xmax':720.,'ytit':'Events'}]
                    elif h == 'phoLeadIDMVA': hd['phoLeadIDMVA'+cstr+sstr] = [{'xtit':'Leading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
                    elif h == 'phoLeadpT': hd['phoLeadpT'+cstr+sstr] = [{'xtit':'Leading photon pT','nb':30,'xmin':0.,'xmax':550.,'ytit':'Events'}]
                    elif h == 'phoLeadEta': hd['phoLeadEta'+cstr+sstr] = [{'xtit':'Leading photon #eta','nb':30,'xmin':-3.,'xmax':3.,'ytit':'Events'}]
                    elif h == 'phoSubLeadIDMVA': hd['phoSubLeadIDMVA'+cstr+sstr] = [{'xtit':'Subleading photon MVA discriminant','nb':30,'xmin':-1.,'xmax':1.,'ytit':'Events'}]
                    elif h == 'phoSubLeadpT': hd['phoSubLeadpT'+cstr+sstr] = [{'xtit':'Subleading photon pT','nb':30,'xmin':0.,'xmax':400.,'ytit':'Events'}]
                    elif h == 'phoSubLeadEta': hd['phoSubLeadEta'+cstr+sstr] = [{'xtit':'Subleading photon #eta','nb':30,'xmin':-3.,'xmax':3.,'ytit':'Events'}]
                    elif h == 'lepDrlpMin': hd['lepDrlpMin'+cstr+sstr] = [{'xtit':'Min #Delta R(l,#gamma)','nb':30,'xmin':0.,'xmax':3.,'ytit':'Events'}]
                    elif h == 'lepPhMllMin': hd['lepPhMllMin'+cstr+sstr] = [{'xtit':'Min m_{Z}-m(l,#gamma))','nb':30,'xmin':0.,'xmax':100.,'ytit':'Events'}]
                    elif h == 'lepPt': hd['lepPt'+cstr+sstr] = [{'xtit':'p_{T}','nb':30,'xmin':0.,'xmax':300.,'ytit':'Events'}]
                    elif h == 'lepEta': hd['lepEta'+cstr+sstr] = [{'xtit':'#eta','nb':30,'xmin':-3.,'xmax':3.,'ytit':'Events'}]
                    elif h == 'lepDeltaRPho': hd['lepDeltaRPho'+cstr+sstr] = [{'xtit':'#Delta R Lepton/Photon','nb':30,'xmin':0.,'xmax':5.,'ytit':'Events'}]
                    elif h == 'topRecMTop': hd['topRecMTop'+cstr+sstr] = [{'xtit':'Reconstructed top mass [GeV]','nb':30,'xmin':0.,'xmax':600.,'ytit':'Events'}]
                    elif h == 'topRecLH': hd['topRecLH'+cstr+sstr] = [{'xtit':'-2 log(P)','nb':30,'xmin':0.,'xmax':3.,'ytit':'Events'}]
                    elif h == 'metPt': hd['metPt'+cstr+sstr] = [{'xtit':'Missing transverse momentum [GeV]','nb':30,'xmin':0.,'xmax':200.,'ytit':'Events'}]
                    elif h == 'evNVtx' : hd['evNVtx'+cstr+sstr] = [{'xtit':'Number of reconstructed vertices','nb':30,'xmin':0.,'xmax':60,'ytit':'Events'}]
                    elif h == 'jet1Pt' : hd['jet1Pt'+cstr+sstr] = [{'xtit':'Jet 1 pT [GeV]','nb':30,'xmin':0.,'xmax':200,'ytit':'Events'}]
                    elif h == 'jet2Pt' : hd['jet2Pt'+cstr+sstr] = [{'xtit':'Jet 2 pT [GeV]','nb':30,'xmin':0.,'xmax':200,'ytit':'Events'}]
                    elif h == 'jet1Eta' : hd['jet1Eta'+cstr+sstr] = [{'xtit':'Jet 1 #eta','nb':30,'xmin':-3.,'xmax':3.,'ytit':'Events'}]
                    elif h == 'jet2Eta' : hd['jet2Eta'+cstr+sstr] = [{'xtit':'Jet 2 #eta','nb':30,'xmin':-3.,'xmax':3.,'ytit':'Events'}]
                    elif h == 'jet1deltaRPho' : hd['jet1deltaRPho'+cstr+sstr] = [{'xtit':'Jet 1 #Delta R Jet/Photon','nb':30,'xmin':0.,'xmax':5.,'ytit':'Events'}]
                    elif h == 'jet1deltaRLep' : hd['jet1deltaRLep'+cstr+sstr] = [{'xtit':'Jet 1 #Delta R Jet/Lepton','nb':30,'xmin':0.,'xmax':5.,'ytit':'Events'}]
                    elif h == 'jet2deltaRPho' : hd['jet2deltaRPho'+cstr+sstr] = [{'xtit':'Jet 2 #Delta R Jet/Photon','nb':30,'xmin':0.,'xmax':5.,'ytit':'Events'}]
                    elif h == 'jet2deltaRLep' : hd['jet2deltaRLep'+cstr+sstr] = [{'xtit':'Jet 2 #Delta R Jet/Lepton','nb':30,'xmin':0.,'xmax':5.,'ytit':'Events'}]


                    else:
                        continue

    outFile = ROOT.TFile.Open(options.output,"RECREATE")

    tfit = {}

    EventId = array( 'i', [ -777 ] )
    DiPhoMassFit, WeightFit = (array( 'd', [ -777 ] ) for _ in range(2))

    for p in ['sig','bkg','data_obs']:
        tfit[p] = ROOT.TTree(p,p)
        tfit[p].Branch("EventId",EventId,"EventId/I");
        tfit[p].Branch("DiPhoMassFit",DiPhoMassFit,"DiPhoMassFit/D");
        tfit[p].Branch("WeightFit",WeightFit,"WeightFit/D");

    for p in tree:
        hist[p] = {}
        for ch, hd in hinfo.items():
            for d in hd:
                for k, v in d.iteritems():
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
            EventId[0] = 0
            for ev in tree[p][s][0]:

                w = eval('ev.evWeight')
                wb = eval('ev.evWeightb')
                mgg = eval('ev.diPhoMass')
                phoLeadIDMVA = eval('ev.phoLeadIDMVA')
                phoSubLeadIDMVA = eval('ev.phoSubLeadIDMVA')
                phoLeadpT = eval('ev.phoLeadpT')
                phoSubLeadpT = eval('ev.phoSubLeadpT')

                nVtx = eval('ev.evNVtx')


                '''if isLep:
                    if phoLeadIDMVA < -0.4 or phoSubLeadIDMVA < -0.4: continue
                else:
                    if phoLeadIDMVA < 0. or phoSubLeadIDMVA < 0.: continue
                '''
                if mgg < 100 or mgg > 180: continue

                if options.blind == '1' and p not in ['StHut','StHct','TtHut','TtHct']:
                    if mgg > 120 and mgg < 130:
                        continue
                elif options.blind == '2' and p in ['data']:
                    if mgg > 120 and mgg < 130:
                        continue

                if p != 'data': w = w * c.lumi / (tree[p][s][2]/tree[p][s][1])

                if math.fabs(w) > 1000 and p in ['Others']: continue # manually remove very large weights

                nBJet = eval('ev.evNBMJet')
                #if nBJet < 1: continue

                DiPhoMassFit[0] = eval('ev.diPhoMass')
                WeightFit[0] = w
                if p in ['data']:
                    tfit['data_obs'].Fill()
                elif p in ['StHut','StHct','TtHut','TtHct']:
#                    if EventId[0] < 2000: #fixme
                    tfit['sig'].Fill()
                    EventId[0] += 1
                else:
                    tfit['bkg'].Fill()

                for k in hist[p]:

                    dec = k.split('_')
                    vname = k.split('_')[0]

                    cname = ''
                    sname = ''
                    if len(dec) > 1:
                        cname = k.split('_')[1]
                    if len(dec) > 2:
                        sname = k.split('_')[2]

                    if isLep:
                        isElec = eval('ev.lepIsElec')
                        if cname == 'Elec':
                            if isElec == False: continue
                        elif cname == 'Muon':
                            if isElec == True: continue

                    nJet = eval('ev.evNJet')
                    if sname == 'SR1':
                        if nJet == 1: continue
                    elif sname == 'SR2':
                        if nJet >= 2: continue

                    br = 'ev.'+vname
                    v = eval(br)
                    hist[p][k].Fill(v,w)

        print ': \033[1;32mdone\033[1;m'

    outFile.Write()
    outFile.Close()
