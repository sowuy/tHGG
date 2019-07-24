#!/bin/env bash
# Submission script
#SBATCH --time=0-05:00:00 # days-hh:mm:ss
#SBATCH --output=plot.txt
#
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=5000 # megabytes
#SBATCH --partition=Def
#SBATCH --qos=normal
#SBATCH --job-name=Plot
#

#names=evNVtx
chan=leptonic
#chan=hadronic
#sl=SR1,SR2
#sl='controlRegion,atLeastOneLepton,atLeastOneJet'
sl=""
#python plot.py \
#--names=diPhoMass \
#--channel=${chan} --blind=2 --selection=${sl}

#--names=diPhoMass,diPhoMVA,phoLeadIDMVA,phoSubLeadIDMVA,metPt

#python plot.py \
#--names=$1 \
#--names=diPhoMass,diPhoPt,phoLeadIDMVA,phoLeadpT,phoLeadEta,phoSubLeadIDMVA,phoSubLeadpT,phoSubLeadEta,lepPt,lepEta,lepDeltaRPho,evNVtx,jet1Pt,jet2Pt,jet1Eta,jet2Eta,jet1deltaRPho,jet1deltaRLep,jet2deltaRPho,jet2deltaRLep \
#--channel=${chan} --selection=${sl}

python plot_backup.py --names=$1 --channel=${chan} --selection=${sl} --output="output_"$1".root"
