# tHGG
tH (H -> gamma gamma) analysis

## From MicroAOD to Ntuple

Analysis is based on the output of
[Ntuplizer](https://github.com/ntuhep/flashggPlugins).

Use CMSSW_10_5_0 release.

```
git clone https://github.com/ntuhep/flashggPlugins
scram b
cd flashggPlugins/flashggAnalysisNtuplizer/test
cmsRun flashggAnalysisNtuplizerWithSyst_cfg.py
```

## Event selection

Ntuples contain all events without any preselection applied. The
[Analyzer](https://github.com/kskovpen/tHGG/tree/master/Analyzer) 
selects events by applying leptonic and hadronic selection criteria
and produces output trees. 

The analysis code does not depend on CMSSW and it can be installed with:

```
git clone https://github.com/kskovpen/tHGG
cd Analyzer
./read.sh
```

## Histograms and higher-level analysis

TBA
