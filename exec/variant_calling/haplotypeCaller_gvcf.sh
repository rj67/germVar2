#!/bin/bash
for i in "$@"
do
case $i in
    -l=*|--bam_file_list=*)
    bam_file="${i#*=}"
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
    ;;
esac
done

echo $bam_file
echo $bed_file

$JAVA_PATH/java -Xmx12g \
  -jar $GATK_PATH/GenomeAnalysisTK.jar \
  -R $REF_PATH/human_g1k_v37.fasta \
  -T HaplotypeCaller \
  --dbsnp $REF_PATH/dbsnp_138.b37.vcf \
  -stand_call_conf 30.0 \
  -stand_emit_conf 30.0 \
  -I $bam_file \
  -minPruning 2  \
  --emitRefConfidence GVCF \
  --variant_index_type LINEAR \
  --variant_index_parameter 128000 \
  --max_alternate_alleles 6 \
  --pcr_indel_model CONSERVATIVE \
  -o $out_dir/$project.raw.gvcf \
  -L $bed_file  \
  -nct 1

