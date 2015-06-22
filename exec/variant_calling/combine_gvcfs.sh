#!/bin/bash

studies=(`ls ./gvcf_lists/*.list | cut -f 3 -d "/" | cut -f 1 -d "_" `)
study=${studies[$1-1]}
input=$study"_gvcf.list"

project='haplo'
ref_dir='/cbio/cslab/home/rj67/resources/Ref_v37'
out_dir='/cbio/cslab/home/rj67/working/haplo_redux/merged_gvcfs'
java_dir='/cbio/cslab/home/leew1/local/jre1.7.0_45/bin'

echo $study
$java_dir/java -Xmx16g \
  -jar /cbio/cslab/home/rj67/local/GenomeAnalysisTK-3.0-0/GenomeAnalysisTK.jar \
  -R $ref_dir/human_g1k_v37.fasta \
  -T CombineGVCFs \
  -V ./gvcf_lists/$input \
  -o $out_dir/$study.merged.gvcf 

