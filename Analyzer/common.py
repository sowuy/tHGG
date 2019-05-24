treeName = "flashggNtuples/flashggStdTree"
workdir = "/user/kskovpen/analysis/tHGGNtuple/CMSSW_10_5_0/src/tHGG/Analyzer/"
proxy = "x509up_u20657"
proxydir = "/user/kskovpen/proxy/"
arch = "slc6_amd64_gcc700"
xmlName = "samples.xml"
batchqueue = "localgrid"
walltime = "06:00:00"

submit = [\
('DoubleEG', -1),\
('DiPhotonJetsBox_M40_80-Sherpa', 303.2),\
('DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa', 84.4),\
('DYToEE_M-50_NNPDF31_13TeV-powheg-pythia8', 21.37),\
('GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8', 232.9),\
('GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8', 3186.0),\
('GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8', 878.1),\
('GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8', 0.11),\
('QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8', 24810.0),\
('QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8', 241400.0),\
('QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8', 118100.0),\
('ST_FCNC-TH_Thadronic_HToaa_eta_hct-MadGraph5-pythia8', 0.019),\
('ST_FCNC-TH_Thadronic_HToaa_eta_hut-MadGraph5-pythia8', 0.139),\
('ST_FCNC-TH_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8', 0.009),\
('ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8', 0.067),\
('TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8', 2.967),\
('THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5', 0.000169),\
('THW_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5', 0.000034),\
('TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hct-MadGraph5-pythia8', 0.230),\
('TT_FCNC-aTtoHJ_Thadronic_HToaa_eta_hut-MadGraph5-pythia8', 0.230),\
('TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8', 0.110),\
('TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8', 0.110),\
('TT_FCNC-T2HJ_aTleptonic_HToaa_eta_hct-MadGraph5-pythia8', 0.110),\
('TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hct-MadGraph5-pythia8', 0.230),\
('TT_FCNC-TtoHJ_aThadronic_HToaa_eta_hut-MadGraph5-pythia8', 0.230),\
('TT_FCNC-TtoHJ_aTleptonic_HToaa_eta_hut-MadGraph5-pythia8', 0.110),\
('TTGG_0Jets_TuneCP5_13TeV_amcatnlo_madspin_pythia8', 0.01687),\
('TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', 3.819),\
('ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8', 0.0016),\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8', 830),\
('VBFHToGG_M125_13TeV_amcatnlo_pythia8', 0.0086),\
('ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8', 50.43)]
