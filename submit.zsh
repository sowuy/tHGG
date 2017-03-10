#!/bin/env zsh

outdir="/user/kskovpen/analysis/tHGG/CMSSW_8_0_25/src/flashgg/Systematics/test/"
queue="localgrid"
ver=("SIG" "BKG" "DATA")
data=("sig_jobs_forthq.json" "bkg_jobs_forthq.json" "data_jobs_forthq.json")
nmax=(-1 -1 -1)
njobs=200

LM=/user/kskovpen/analysis/tHGG/CMSSW_8_0_25/src/flashgg/Systematics/test/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt

cp /tmp/x509up_u20657 /user/kskovpen/proxy/x509up_u20657
export X509_USER_PROXY=/user/kskovpen/proxy/x509up_u20657

idx=0
for i in $data
do

idx=$[$idx+1]

if [[ ${ver[$idx]} != "SIG" ]]; then
  continue
fi

echo "##################### ${ver[$idx]} #####################"

rm -rf flat${ver[$idx]}
mkdir flat${ver[$idx]}

if [[ ${ver[$idx]} != "DATA" ]]; then

fggRunJobs.py \
--load ${i} \
-d $outdir/flat${ver[$idx]}/jobs \
-x cmsRun workspaceStd_testThq.py \
maxEvents=${nmax[$idx]} \
-n ${njobs} \
-D \
-b sge \
-q $queue \
--no-use-tarball  \
--no-copy-proxy \
puTarget=2.51e+05,1.15e+06,2.47e+06,3.72e+06,5.19e+06,6.79e+06,8.67e+06,2.31e+07,5.89e+07,1.38e+08,3.12e+08,5.71e+08,8.76e+08,1.21e+09,1.56e+09,1.87e+09,2.08e+09,2.19e+09,2.24e+09,2.28e+09,2.29e+09,2.24e+09,2.15e+09,2.03e+09,1.88e+09,1.71e+09,1.54e+09,1.36e+09,1.19e+09,1.01e+09,8.48e+08,6.94e+08,5.57e+08,4.38e+08,3.37e+08,2.53e+08,1.85e+08,1.31e+08,8.96e+07,5.87e+07,3.68e+07,2.2e+07,1.25e+07,6.75e+06,3.46e+06,1.68e+06,7.79e+05,3.44e+05,1.46e+05,6.13e+04,2.68e+04,1.33e+04,8.25e+03,6.3e+03,5.45e+03,4.97e+03,4.59e+03,4.25e+03,3.92e+03,3.58e+03,3.25e+03,2.93e+03,2.62e+03,2.33e+03,2.05e+03,1.79e+03,1.56e+03,1.34e+03,1.14e+03,969,815,680,563,463,378

else

fggRunJobs.py \
--load ${i} \
-d $outdir/flat${ver[$idx]}/jobs \
-x cmsRun workspaceStd_testThq.py \
maxEvents=${nmax[$idx]} \
-n ${njobs} \
-D \
-b sge \
-q $queue \
--no-use-tarball  \
--no-copy-proxy \
puTarget=2.51e+05,1.15e+06,2.47e+06,3.72e+06,5.19e+06,6.79e+06,8.67e+06,2.31e+07,5.89e+07,1.38e+08,3.12e+08,5.71e+08,8.76e+08,1.21e+09,1.56e+09,1.87e+09,2.08e+09,2.19e+09,2.24e+09,2.28e+09,2.29e+09,2.24e+09,2.15e+09,2.03e+09,1.88e+09,1.71e+09,1.54e+09,1.36e+09,1.19e+09,1.01e+09,8.48e+08,6.94e+08,5.57e+08,4.38e+08,3.37e+08,2.53e+08,1.85e+08,1.31e+08,8.96e+07,5.87e+07,3.68e+07,2.2e+07,1.25e+07,6.75e+06,3.46e+06,1.68e+06,7.79e+05,3.44e+05,1.46e+05,6.13e+04,2.68e+04,1.33e+04,8.25e+03,6.3e+03,5.45e+03,4.97e+03,4.59e+03,4.25e+03,3.92e+03,3.58e+03,3.25e+03,2.93e+03,2.62e+03,2.33e+03,2.05e+03,1.79e+03,1.56e+03,1.34e+03,1.14e+03,969,815,680,563,463,378 \
lumiMask=${LM}

fi

done
