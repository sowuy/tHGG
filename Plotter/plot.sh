#!/bin/env bash

#chan=leptonic
chan=hadronic
#sl=SR1,SR2
sl=''

python plot.py \
--names=diPhoMass --channel=${chan} --blind=1 --selection=${sl}

#--names=diPhoMass,diPhoMVA,phoLeadIDMVA,phoSubLeadIDMVA,metPt
