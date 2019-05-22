#!/bin/sh

export X509_USER_PROXY=/user/kskovpen/proxy/x509up_u20657

WDIR=$(pwd)

dout=${dout}
sample=${sample}
output=${output}
nmax=${nmax}

export ROOTSYS=/cvmfs/cms.cern.ch/slc6_amd64_gcc700/lcg/root/6.12.07-dlmfga
ls $ROOTSYS/bin/thisroot.sh
source $ROOTSYS/bin/thisroot.sh
rootV=$(root-config --version)
echo "ROOT v${rootV} has been set up"

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${dout}/../:${dout}/../obj

export LD_LIBRARY_PATH=\
/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/gcc/7.0.0-omkpbe2/lib64:\
/usr/lib64:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/gcc/7.0.0-omkpbe2/lib:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_5_0/external/slc6_amd64_gcc700/lib/:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_5_0/lib/slc6_amd64_gcc700/:\
$LD_LIBRARY_PATH

export PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/gcc/7.0.0-omkpbe2/bin:$PATH

echo "Executing python read.py --sample ${sample} --output ${output} --nmax ${nmax}"
time python ${dout}/./read.py --sample "${sample}" --output "${output}" --nmax "${nmax}"
