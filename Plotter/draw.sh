#!/bin/env bash

#pn="_Muon"
pn="_All"
#sl="_SelNJet2"
sl=""

python draw.py \
--names=diPhoMass${pn}${sl},\
diPhoMVA${pn}${sl},\
lepPhMllMin${pn}${sl},\
phoLeadIDMVA${pn}${sl},\
phoSubLeadIDMVA${pn}${sl} \
--channel=leptonic --factor=1
