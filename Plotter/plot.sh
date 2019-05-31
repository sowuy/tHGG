#!/bin/env bash

python plot.py \
--names=diPhoMass,diPhoMVA,phoLeadIDMVA,phoSubLeadIDMVA,lepPhMllMin \
--channel=leptonic --blind=1 --selection=SelNJet2
