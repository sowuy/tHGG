#!/bin/env bash

#pn="_Muon"
pn="_All"
#pn=""
#sl="_SR2"
sl=""
ch=leptonic
#ch=hadronic

python draw.py \
--names=diPhoMass${pn}${sl},\
diPhoMVA${pn}${sl},\
phoLeadIDMVA${pn}${sl},\
metPt${pn}${sl},\
phoSubLeadIDMVA${pn}${sl} \
--channel=${ch} --factor=1
