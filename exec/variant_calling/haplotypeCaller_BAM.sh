#!/bin/bash

for i in "$@"
do
case $i in
    -l=*|--bam_file_list=*)
    bam_list="${i#*=}"
    shift
    ;;
    -b=*|--bed_region_file=*)
    bed_file="${i#*=}"
    shift
    ;;
    -o=*|--output_directory=*)
    out_dir="${i#*=}"
    shift
    ;;
    -n=*|--project_name=*)
    project="${i#*=}"
    shift
    ;;
    *)
            # unknown option
    ;;
esac
done

# make sure out_dir is a directory, no trailing \
#out_dir=`dirname $out_dir`

$JAVA_PATH/java -Xmx12g \
  -jar $GATK_PATH/GenomeAnalysisTK.jar \
  -R $REF_PATH/human_g1k_v37.fasta \
  -T HaplotypeCaller \
  --dbsnp $REF_PATH/dbsnp_138.b37.vcf \
  -stand_call_conf 30.0 \
  -stand_emit_conf 0.0 \
  -I $bam_list \
  -minPruning 2  \
  --maxNumHaplotypesInPopulation 256 \
  --max_alternate_alleles 6 \
  --pcr_indel_model CONSERVATIVE \
  -o $out_dir/$project.haplo.vcf \
  -L $bed_file \
  -nct 4 \

cat $out_dir/$project.haplo.vcf | vcfAnnoAlt.py | sed '1,/^##/d' | vcfbreakmulti | $BCFTOOLS_PATH/bcftools norm -f $REF_PATH/human_g1k_v37.fasta -O v - | \
    $JAVA_PATH/java -jar $SNPEFF_PATH/SnpSift.jar varType - | vcflength  > $out_dir/$project.split.vcf 
  

