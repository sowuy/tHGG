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

The list of produced ntuples can be found
[here](https://github.com/kskovpen/tHGG/blob/master/Analyzer/samples.xml).
It can be created with:

```
python samples.py --version=Flatfish-v20190514
```

## Event selection

Ntuples contain all events without any preselection applied. The
[Analyzer](https://github.com/kskovpen/tHGG/tree/master/Analyzer) 
selects events by applying leptonic and hadronic selection criteria
and produces output trees. 

The analysis code does not depend on CMSSW and it can be run with:

```
git clone https://github.com/kskovpen/tHGG
cd tHGG/Analyzer
./read.sh
```

Available run options:

```
python read.py -h
```

Submit jobs to local batch:

```
python submit.py
```

The batch configuration and sample list can be found in
[common.py](https://github.com/kskovpen/tHGG/blob/master/Analyzer/common.py).

## Histograms and higher-level analysis

An example of histogram creation:

```
cd tHGG/Plotter
python plot.py --channel=leptonic --names=diPhoMass,phoLeadPt 
```

The plotting configuration is available in
[common.py](https://github.com/kskovpen/tHGG/blob/master/Plotter/common.py).
