#!/bin/env bash

#pn="_Muon"
#pn="_Elec"
pn="_All"
#pn=""
#sl="_SR1"
sl=""
#ch=leptonic
ch=hadronic

#python draw.py \
#--names=evNVtx${pn}${sl} \
#--channel=${ch}


#--names=evNVtx${pn}${sl},diPhoMass${pn}${sl},diPhoPt${pn}${sl},phoLeadpT${pn}${sl},\
#phoLeadEta${pn}${sl},phoLeadIDMVA${pn}${sl},phoSubLeadpT${pn}${sl},phoSubLeadEta${pn}${sl},\
#phoSubLeadIDMVA${pn}${sl},lepPt${pn}${sl},lepEta${pn}${sl},\
#lepDeltaRLeadPho${pn}${sl},lepDeltaRSubLeadPho${pn}${sl},\
#jet1Pt${pn}${sl},jet2Pt${pn}${sl},jet1Eta${pn}${sl},jet2Eta${pn}${sl},\
#jet1deltaRLeadPho${pn}${sl},jet1deltaRSubLeadPho${pn}${sl},jet1deltaRLep${pn}${sl},jet2deltaRLeadPho${pn}${sl},jet2deltaRSubLeadPho${pn}${sl},\
#lepDeltaRHiggs${pn}${sl},jet1deltaRHiggs${pn}${sl},jet2deltaRHiggs${pn}${sl} \

python draw.py \
--names=evNVtx${pn}${sl},diPhoMass${pn}${sl},diPhoPt${pn}${sl},phoLeadpT${pn}${sl},\
phoLeadEta${pn}${sl},phoLeadIDMVA${pn}${sl},phoSubLeadpT${pn}${sl},phoSubLeadEta${pn}${sl},\
phoSubLeadIDMVA${pn}${sl},\
jet1Pt${pn}${sl},jet2Pt${pn}${sl},jet1Eta${pn}${sl},jet2Eta${pn}${sl},jet1deltaRPho${pn}${sl},\
jet2deltaRPho${pn}${sl} \
--channel=${ch} \
--input=results/allHistos_Had.root \
--output=pics_Had
