#!/usr/bin/env python

###################################################################

#vcfAnnoSTR: annotate 3prime side  sequence and possible STR 

###################################################################

import vcf
import sys
import subprocess 
import argparse
from vcf.parser import _Info as VcfInfo

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=' vcfAnnoSTR')
  parser.add_argument('--ref','-r',
                    required=True,
                    help="Fasta file for the genomic reference")
  parser.add_argument('--anc_ref','-a',
                    required=True,
                    help="Fasta file for the ancester genomic reference")
  args = parser.parse_args()
  
  vcf_reader = vcf.Reader(sys.stdin)
  
  vcf_reader.infos['ALT_Codon'] = VcfInfo( 'ALT_Codon', 1, 'String', 'Alt codon')
  vcf_reader.infos['ANC_Codon'] = VcfInfo( 'ANC_Codon', 1, 'String', 'Ancester allele codon')
  
  writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')
  
  for Record in vcf_reader:
    
    if Record.INFO.get('LoF_filter', False):
      if 'ANC_ALLELE' in Record.INFO['LoF_filter'] :
        if  Record.INFO['VARTYPE'] == 'SNP' :
          
          phase = int(Record.INFO['CDS_position'].split('|')[0]) % 3
          strand = Record.INFO['STRAND'].split('|')[0]
    
          # use samtools faidx to extract 
          if strand ==  '-1':
            ranges = [Record.POS - phase, Record.POS + 2 - phase ]
            pos = (3-phase) % 3
          elif strand ==  '1':
            ranges = [Record.POS + phase - 2 , Record.POS+ phase ]
            pos = (phase +2) % 3
          
          region = " " + Record.CHROM + ':' + str(ranges[0]) + '-' + str(ranges[1])
          
          anc_ref = subprocess.check_output("samtools faidx "+args.anc_ref + region, shell=True)
          anc_ref = anc_ref.splitlines()[1]
          
          ref = subprocess.check_output("samtools faidx "+args.ref + region, shell=True)
          ref = ref.splitlines()[1]
          
          alt = ref[0:pos] + Record.ALT[0].sequence + ref[pos+1:]
          #print Record.REF, Record.ALT[0], ref, alt, anc_ref
          Record.add_info('ALT_Codon', alt)
          Record.add_info('ANC_Codon', anc_ref)
          
    writer.write_record(Record)
