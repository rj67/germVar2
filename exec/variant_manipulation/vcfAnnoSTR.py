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
  parser.add_argument('--length','-l',
                    type=int,
                    default=25,
                    help="length of sequence on the 3 prime side")
  parser.add_argument('--thresh_times','-t',
                    type=int,
                    default=5,
                    help="times of repeat above which STR is called")
  args = parser.parse_args()
  
  vcf_reader = vcf.Reader(sys.stdin)
  
  vcf_reader.infos['Primer3'] = VcfInfo( 'Primer3', 1, 'String', '3 prime side sequence')
  vcf_reader.infos['Primer5'] = VcfInfo( 'Primer5', 1, 'String', '5 prime side sequence')
  vcf_reader.infos['STR'] = VcfInfo( 'STR', 0, 'Flag', 'whether there is STR')
  vcf_reader.infos['STR_RU'] = VcfInfo( 'STR_RU', 1, 'String', 'repeating unit of STR')
  vcf_reader.infos['STR_times'] = VcfInfo( 'STR_times', 1, 'Integer', 'time of repeats for STR')
  vcf_reader.infos['STR_match'] = VcfInfo( 'STR_match', 0, 'Flag', 'whether the ALT sequence change from REF matches multiples of STR_RU')
  
  writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')
  
  for Record in vcf_reader:
    
    # use samtools faidx to extract 5' and 3' sequence
    region3 = " " + Record.CHROM + ':' + str(Record.POS + 1) + '-' + str(Record.POS + args.length)
    primer3 = subprocess.check_output("samtools faidx "+args.ref + region3, shell=True)
    primer3 = primer3.splitlines()[1]
    Record.add_info('Primer3', primer3)
    
    region5 = " " + Record.CHROM + ':' + str(Record.POS - args.length) + '-' + str(Record.POS - 1)
    primer5 = subprocess.check_output("samtools faidx "+args.ref + region5, shell=True)
    primer5 = primer5.splitlines()[1]
    Record.add_info('Primer5', primer5)
    
    # test whether 3 primer has more than x number of repeats, where the repeating unit is of length up to 5
    STR = False
    RU_length = 1
    while not STR and RU_length <= 5 :  
      if primer3.startswith(primer3[0:RU_length]*args.thresh_times) :
        STR = True
        STR_RU = primer3[0:RU_length]
      RU_length += 1

    # figure out the number of times the RU repeats
    if STR :
      STR_times = max([i for i in range(args.thresh_times, len(primer3)//len(STR_RU)+1) if primer3.startswith(STR_RU*i)])
      Record.add_info('STR', STR)
      Record.add_info('STR_RU', STR_RU)
      Record.add_info('STR_times', STR_times)
      
      # rely on SnpSift VARTYPE annotation
      if "INS" in Record.INFO['VARTYPE'] or "DEL" in Record.INFO['VARTYPE'] :
    
        if "INS" in Record.INFO['VARTYPE'] :
          alt_sequence = Record.ALT[0].sequence[len(Record.REF):]
        else:
          alt_sequence = Record.REF[len(Record.ALT[0].sequence):]
        
        # see if alt sequence is multiple of STR_RU
        if len(alt_sequence) % len(STR_RU) == 0 :
          if alt_sequence == STR_RU * (len(alt_sequence) / len(STR_RU)) :
            Record.add_info('STR_match', True)
            
    writer.write_record(Record)
