#!/bin/bash

study=$1

in_dir='/cbio/cslab/home/rj67/vcf/merged_gvcfs'
out_dir='/cbio/cslab/home/rj67/vcf/batch_vcfs'
Map_file='/cbio/cslab/home/rj67/resources/Mapability/wgEncodeCrgMapabilityAlign75mer_exome.bedGraph' 

#$JAVA_PATH/java -Xmx12g \
#  -jar $GATK_PATH/GenomeAnalysisTK.jar \
#  -R $REF_PATH/human_g1k_v37.fasta \
#  -T GenotypeGVCFs \
#  --dbsnp $REF_PATH/dbsnp_138.b37.vcf \
#  -V $in_dir/$study.merged.gvcf \
#  -o $out_dir/$study.batch.vcf \
#  -nt 1 

# split multiallelic variants, annotate
cat $out_dir/$study.batch.vcf | vcfAnnoAlt.py | sed '1,/^##/d' | \
  vcfbreakmulti | $BCFTOOLS_PATH/bcftools norm -f $REF_PATH/human_g1k_v37.fasta -O v - | \
  $JAVA_PATH/java -jar $SNPEFF_PATH/SnpSift.jar varType - | vcfTrimMNP.py  | sed '1,/^##/d' | vcflength | \
  $JAVA_PATH/java -Xmx4g -jar $SNPEFF_PATH/snpEff.jar  -c $SNPEFF_PATH/snpEff.config  \
  -noStats -t -no-downstream -no-upstream -no-intergenic -no-utr -no-intron -no REGULATION -onlyTr $REF_PATH/list_goi_GRCh37.75_CCDS_transcript.txt -v GRCh37.75 - | \
  $SNPEFF_PATH/scripts/vcfEffOnePerLine.pl | grep -v 'EFF=sequence_feature'  | vcfConvSnpEff.py | sed '1,/^##/d' |  \
  $JAVA_PATH/java -jar $SNPEFF_PATH/SnpSift.jar annotate -id $REF_PATH/dbsnp_138.b37.vcf - | \
  vcfAnnoSTR.py -r $REF_PATH/human_g1k_v37.fasta  | sed '1,/^##/d' | \
  vcfannotate -b $Map_file -k Mappability > $out_dir/$study.batch.anno.vcf


#cat $out_dir/$study.joint.vcf | vcfAnnoAlt.py | vcfbreakmulti | $bcftools_dir/bcftools norm -f $ref_dir/human_g1k_v37.fasta -O v - | \
# $java_dir/java -jar $snpEff_dir/SnpSift.jar varType - | vcfTrimMNP.py  | \
# $java_dir/java -Xmx4g -jar $snpEff_dir/snpEff.jar  -c $snpEff_dir/snpEff.config  \
#     -noStats -t -canon -no-downstream -no-upstream -no-intergenic -v GRCh37.74 -  | \
#  $snpEff_dir/scripts/vcfEffOnePerLine.pl | vcfConvSnpEff.py | vcfSelExon.py | \
# $java_dir/java -jar $snpEff_dir/SnpSift.jar annotate -noId -info 1kG_AF $X1kG_dir/ALL.wgs.phase1_release_v3.20101123.snps_indels.sites.vcf - | \
# vcfAnnoPfam.py  > $out_dir/$study.anno.vcf
#
#vcffilter -f "Impact = HIGH" -f "QD > 1."  $out_dir/$study.anno.vcf | awk '{OFS="\t"; if (!/^#/){print $1,$2-1,$2}}' >  $out_dir/$study.high.bed
