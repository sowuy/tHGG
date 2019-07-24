lumi = 41530


path = '../Analyzer/jobs/'


process = {\
'data':('DoubleEG',),\
'StHut':('ST_FCNC-TH_Thadronic_HToaa_eta_hut-MadGraph5-pythia8',\
         'ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8'),\
'TtHut':('TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hut-MadGraph5-pythia8',\
         'TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hut-MadGraph5-pythia8',\
         'TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8',\
         'TT_FCNC-TtoHJ_aTleptonic_HToaa_eta_hut-MadGraph5-pythia8'),\
'StHct':('ST_FCNC-TH_Thadronic_HToaa_eta_hct-MadGraph5-pythia8',\
         'ST_FCNC-TH_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8'),\
'TtHct':('TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hct-MadGraph5-pythia8',\
         'TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hct-MadGraph5-pythia8',\
         'TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8',\
         'TT_FCNC-T2HJ_aTleptonic_HToaa_eta_hct-MadGraph5-pythia8'),\
'DiPhotonJets':('DiPhotonJetsBox_M40_80-Sherpa',\
                'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa'),\
'TGJets':('TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8',),\
'TTGJets':('TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',\
           'TTGG_0Jets_TuneCP5_13TeV_amcatnlo_madspin_pythia8'),\
'GJet':('GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
        'GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',\
        'GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8'),\
'Higgs':('GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8',\
         'ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8',\
         'VBFHToGG_M125_13TeV_amcatnlo_pythia8',\
         'THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5',\
         'THW_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5'),\
'VJets':('ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8',\
        'DYToEE_M-50_NNPDF31_13TeV-powheg-pythia8'),\
'QCD':('QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
       'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',\
       'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8'),\
'TT':('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',)
}

processSort = []
processSort.append('data')
processSort.append('DiPhotonJets')
processSort.append('GJet')
processSort.append('QCD')
processSort.append('TT')
processSort.append('TGJets')
processSort.append('TTGJets')
processSort.append('VJets')
processSort.append('Higgs')
processSort.append('TtHut')
processSort.append('StHut')
processSort.append('TtHct')
processSort.append('StHct')
