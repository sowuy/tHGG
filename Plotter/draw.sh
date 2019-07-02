#!/bin/env bash

#pn="_Elec"
pn="_All"
#pn=""
#sl="_SR1"
sl=""
ch=leptonic
#ch=hadronic

#--names=diPhoMass${pn}${sl},phoLeadIDMVA${pn}${sl},phoSubLeadIDMVA${pn}${sl},diPhoMVA${pn}${sl} \

python draw.py \
--names=diPhoMass${pn}${sl} \
--channel=${ch} --factor=0.1
