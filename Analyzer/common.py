treeName = "flashggNtuples/flashggStdTree"
workdir = "/user/kskovpen/analysis/tHGGNtuple/CMSSW_10_5_0/src/tHGG/Analyzer/"
proxy = "x509up_u20657"
proxydir = "/user/kskovpen/proxy/"
arch = "slc6_amd64_gcc700"
xmlName = "samples.xml"
batchqueue = "localgrid"
walltime = "03:00:00"

submit = [\
('DoubleEG',-1),\
('DiPhotonJetsBox_M40_80-Sherpa',777),\
('DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa',777),\
('DYToEE_M-50_NNPDF31_13TeV-powheg-pythia8',777),\
('GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',777),\
('GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',777),\
('GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',777),\
('GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8',777),\
('QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',777),\
('QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',777),\
('QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',777),\
('ST_FCNC-TH_Thadronic_HToaa_eta_hct-MadGraph5-pythia8',777),\
('ST_FCNC-TH_Thadronic_HToaa_eta_hut-MadGraph5-pythia8',777),\
('ST_FCNC-TH_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8',777),\
('ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8',777),\
('TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8',777),\
('THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5',777),\
('THW_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5',777),\
('TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hct-MadGraph5-pythia8',777),\
('TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hut-MadGraph5-pythia8',777),\
('TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8',777),\
('TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8',777),\
('TT_FCNC-T2HJ_aTleptonic_HToaa_eta_hct-MadGraph5-pythia8',777),\
('TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hct-MadGraph5-pythia8',777),\
('TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hut-MadGraph5-pythia8',777),\
('TT_FCNC-TtoHJ_aTleptonic_HToaa_eta_hut-MadGraph5-pythia8',777),\
('TTGG_0Jets_TuneCP5_13TeV_amcatnlo_madspin_pythia8',777),\
('TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',777),\
('ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8',777),\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',777),\
('VBFHToGG_M125_13TeV_amcatnlo_pythia8',777),\
('ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8',777)]
