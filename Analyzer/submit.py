import os
import sys
import xml.etree.ElementTree as ET
import common as c

samples = [\
'DiPhotonJetsBox_M40_80-Sherpa',\
'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa',\
'DYToEE_M-50_NNPDF31_13TeV-powheg-pythia8',\
'GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
'GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',\
'GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
'GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8',\
'QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',\
'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
'ST_FCNC-TH_Thadronic_HToaa_eta_hct-MadGraph5-pythia8',\
'ST_FCNC-TH_Thadronic_HToaa_eta_hut-MadGraph5-pythia8',\
'ST_FCNC-TH_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8',\
'ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8',\
'TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8',\
'THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5',\
'THW_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5',\
'TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hct-MadGraph5-pythia8',\
'TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hut-MadGraph5-pythia8',\
'TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8',\
'TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8',\
'TT_FCNC-T2HJ_aTleptonic_HToaa_eta_hct-MadGraph5-pythia8',\
'TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hct-MadGraph5-pythia8',\
'TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hut-MadGraph5-pythia8',\
'TT_FCNC-TtoHJ_aTleptonic_HToaa_eta_hut-MadGraph5-pythia8',\
'TTGG_0Jets_TuneCP5_13TeV_amcatnlo_madspin_pythia8',\
'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',\
'ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8',\
'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',\
'VBFHToGG_M125_13TeV_amcatnlo_pythia8',\
'ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8']

files=[]
xmlTree = ET.parse(c.xmlName)
for s in xmlTree.findall('sample'):
    for s0 in samples:
        if s.get('id') == s0:
            isdata = s.get('isdata')
            for child in s:
                files.append(child.text)
