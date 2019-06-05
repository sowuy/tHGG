#!/bin/env bash

nmax=10000

#python read.py --sample=TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8 \
#--output=output.root --nmax=${nmax} --xml=samples.xml

#python read.py --sample=TT_FCNC-TtoHJ_aTleptonic_HToaa_eta_hut-MadGraph5-pythia8 \
#--output=output.root --nmax=${nmax} --xml=jobs/TT_FCNC-TtoHJ_aTleptonic_HToaa_eta_hut-MadGraph5-pythia8/TT_FCNC-TtoHJ_aTleptonic_HToaa_eta_hut-MadGraph5-pythia8_0.xml

#python read.py --sample=ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8 \
#--output=output.root --nmax=${nmax} --xml=jobs/ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8/ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8_0.xml

python read.py --sample=ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8 --run='' \
--output=output.root --toprec=1 --nmax=${nmax} --xml=jobs/ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8/ST_FCNC-TH_Tleptonic_HToaa_eta_hut-MadGraph5-pythia8_0.xml

#python read.py --sample=DoubleEG \
#--output=output.root --nmax=${nmax} --xml=samples.xml
