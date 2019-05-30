#!/bin/env bash

pn="_Elec"

python draw.py --names=diPhoMass${pn},diPhoMVA${pn},phoLeadIDMVA${pn},phoSubLeadIDMVA${pn} --channel=leptonic --factor=1
