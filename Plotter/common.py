lumi = 41530

datapath = '../Analyzer/jobs/'

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
'TTJets':('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',\
          'TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8',\
          'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',\
          'TTGG_0Jets_TuneCP5_13TeV_amcatnlo_madspin_pythia8'),\
'QCD':('QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
       'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',\
       'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8'),\
'GJet':('GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',\
        'GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',\
        'GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8')\
}

processSort = []
processSort.append('data')
processSort.append('DiPhotonJets')
processSort.append('TTJets')
processSort.append('GJet')
processSort.append('QCD')
processSort.append('TtHut')
processSort.append('StHut')
processSort.append('TtHct')
processSort.append('StHct')
