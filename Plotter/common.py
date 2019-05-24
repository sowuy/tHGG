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
                'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa')}

processSort = []
processSort.append('data')
processSort.append('DiPhotonJets')
processSort.append('TtHut')
processSort.append('StHut')
processSort.append('TtHct')
processSort.append('StHct')
