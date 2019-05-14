#!/bin/env zsh

slist="data.txt"
pset="crabConfigTemplate.py"
ver="Flatfish-v20190514"
prodv="/store/user/kskovpen/tHGG/Ntuple/${ver}/"

#mv ../../../../src/flashgg/Taggers/data/DNN_models ../../../../../.

rm -f crabConfig.py*

samp=()
is=1
cat ${slist} | while read line
do
  samp[${is}]=${line}
  is=$[$is+1]
done

for i in ${samp}
do
  spl=($(echo $i | tr "/" "\n"))
  pubdn=$(echo "${spl[2]}_${spl[3]}" | sed 's%-%_%g')
  nam=$(echo "${spl[1]}" | sed 's%-%_%g')
  reqn=$(echo "${nam}_${pubdn}" \
  | sed 's%_31Mar.*%%g' | sed 's%RunIIFall18_4_0_0_44_g36175afd_v0_%%g' | sed 's%kskovpen_2017_v20190402_%%g' \
  | sed 's%_RunIIFall17.*%%g')
  cat ${pset} | sed "s%INPUTDATASET%${i}%g" \
  | sed "s%OUTLFN%${prodv}%g" \
  | sed "s%REQUESTNAME%${reqn}%g" \
  | sed "s%PUBLISHDATANAME%${pubdn}%g" \
  > crabConfig.py
  
  echo "${reqn}"
  crab submit
  
done

rm -f crabConfig.py*
