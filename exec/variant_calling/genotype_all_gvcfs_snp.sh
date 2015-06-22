#!/bin/bash

#chrs=(`cut -f 1 $bed_prefix.bed | sort | uniq `)
#chr=${chrs[$1-1]}
#echo $chr
chr=$1

# I/O
project='norm_nsSNP'
out_dir='/home/rj67/group/results/Aug_5'
in_dir='/home/rj67/group/results/merged_gvcf'
bed_prefix='split_bed/nsSNP.MHS_Clinvar'

out_file=$project.$chr
# reference file
Map_file='/home/rj67/seq/Mapability/wgEncodeCrgMapabilityAlign75mer_exome.bedGraph' 

$JAVA_PATH/java -Xmx12g \
  -jar $GATK_PATH/GenomeAnalysisTK.jar \
  -R $REF_PATH/human_g1k_v37.fasta \
  -T GenotypeGVCFs \
  --dbsnp $REF_PATH/dbsnp_138.b37.vcf \
  -V $in_dir/ACC_1.merged.gvcf  \
  -V $in_dir/BLCA_1.merged.gvcf\
  -V $in_dir/BLCA_2.merged.gvcf\
  -V $in_dir/BRCA_1.merged.gvcf\
  -V $in_dir/BRCA_2.merged.gvcf\
  -V $in_dir/BRCA_3.merged.gvcf\
  -V $in_dir/BRCA_4.merged.gvcf\
  -V $in_dir/CESC_1.merged.gvcf\
  -V $in_dir/COAD_1.merged.gvcf\
  -V $in_dir/ESCA_1.merged.gvcf\
  -V $in_dir/GBM_1.merged.gvcf\
  -V $in_dir/GBM_2.merged.gvcf\
  -V $in_dir/HNSC_1.merged.gvcf\
  -V $in_dir/HNSC_2.merged.gvcf\
  -V $in_dir/KICH_1.merged.gvcf\
  -V $in_dir/KIRC_1.merged.gvcf\
  -V $in_dir/KIRC_2.merged.gvcf\
  -V $in_dir/KIRP_1.merged.gvcf\
  -V $in_dir/LGG_1.merged.gvcf\
  -V $in_dir/LGG_2.merged.gvcf\
  -V $in_dir/LIHC_1.merged.gvcf\
  -V $in_dir/LUAD_1.merged.gvcf\
  -V $in_dir/LUAD_2.merged.gvcf\
  -V $in_dir/LUAD_3.merged.gvcf\
  -V $in_dir/LUSC_1.merged.gvcf\
  -V $in_dir/LUSC_2.merged.gvcf\
  -V $in_dir/OV_1.merged.gvcf\
  -V $in_dir/OV_2.merged.gvcf\
  -V $in_dir/PAAD_1.merged.gvcf\
  -V $in_dir/PCPG_1.merged.gvcf\
  -V $in_dir/PRAD_1.merged.gvcf\
  -V $in_dir/PRAD_2.merged.gvcf\
  -V $in_dir/READ_1.merged.gvcf\
  -V $in_dir/SARC_1.merged.gvcf\
  -V $in_dir/SKCM_1.merged.gvcf\
  -V $in_dir/SKCM_2.merged.gvcf\
  -V $in_dir/STAD_1.merged.gvcf\
  -V $in_dir/STAD_2.merged.gvcf\
  -V $in_dir/THCA_1.merged.gvcf\
  -V $in_dir/THCA_2.merged.gvcf\
  -V $in_dir/UCEC_1.merged.gvcf\
  -V $in_dir/UCEC_2.merged.gvcf\
  -V $in_dir/UCS_1.merged.gvcf\
  -o $out_dir/$out_file.vcf \
  -nt 1 \
  -L $REF_PATH/$bed_prefix.$chr.bed 

# split multiallelic variants, put into GT vcf file.
cat $out_dir/$out_file.vcf | vcfAnnoAlt.py | sed '1,/^##/d' | \
  vcfbreakmulti | $BCFTOOLS_PATH/bcftools norm -f $REF_PATH/human_g1k_v37.fasta -O v - | \
  $JAVA_PATH/java -jar $SNPEFF_PATH/SnpSift.jar varType - | vcfTrimMNP.py  | sed '1,/^##/d' | \
  vcfkeepgeno - "GT" "AD" "DP" > $out_dir/$out_file.GT.vcf

## remove the genotype information, annotate variant
$BCFTOOLS_PATH/bcftools view -G $out_dir/$out_file.GT.vcf | vcflength | \
 $JAVA_PATH/java -Xmx4g -jar $SNPEFF_PATH/snpEff.jar  -c $SNPEFF_PATH/snpEff.config  \
  -noStats -t -no-downstream -no-upstream -no-intergenic -no-utr -no-intron -no REGULATION -onlyTr $REF_PATH/list_goi_GRCh37.75_long_transcript.txt -v GRCh37.75 - | \
 $SNPEFF_PATH/scripts/vcfEffOnePerLine.pl | grep -v 'EFF=sequence_feature'  | vcfConvSnpEff.py | sed '1,/^##/d' |  \
 $JAVA_PATH/java -jar $SNPEFF_PATH/SnpSift.jar annotate -id $REF_PATH/dbsnp_138.b37.vcf - | \
 vcfannotate -b $Map_file -k Mappability | vcfFixAllele.py | sed '1,/^##/d' >  $out_dir/$out_file.VAR.vcf

# for snp
#perl $VEP_PATH/variant_effect_predictor.pl --cache --offline --sift b -polyphen b --humdiv --ccds --uniprot  --hgvs --symbol --numbers --canonical --protein --biotype -coding_only \
#    --no_stats  -i  $out_dir/$out_file.tmp.vcf -vcf -o STDOUT | vcfConvVEP.py | sed '1,/^##/d' | vcfFixAllele.py | sed '1,/^##/d' >  $out_dir/$out_file.VAR.vcf

#perl $VEP_PATH/variant_effect_predictor.pl --cache --offline --everything --humdiv --no_stats --coding_only --plugin LoF,human_ancestor_fa:/home/rj67/.vep/Plugins/human_ancestor.fa.gz  \
#  -i  $out_dir/$project.$chr.tmp.vcf -vcf -o STDOUT | vcfConvVEP.py | sed '1,/^##/d' | vcfFixAllele.py | sed '1,/^##/d' > $out_dir/$project.$chr.VAR.vcf

sed -i '1s/^/##fileformat=VCFv4.1\n/' $out_dir/$out_file.VAR.vcf
sed -i '1s/^/##fileformat=VCFv4.1\n/' $out_dir/$out_file.GT.vcf
