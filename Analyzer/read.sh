#!/bin/env bash

nmax=1000

python read.py --sample=TT_FCNC-aTtoHJ_Tleptonic_HToaa_eta_hct-MadGraph5-pythia8 \
--output=output.root --nmax=${nmax}
