#!/bin/env bash

nmax=10000

#python read.py --sample=TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8 \
#--output=output.root --nmax=${nmax} --xml=samples.xml

python read.py --sample=TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8 \
--output=output.root --nmax=${nmax} --xml=jobs/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_0.xml

#python read.py --sample=DoubleEG \
#--output=output.root --nmax=${nmax} --xml=samples.xml
