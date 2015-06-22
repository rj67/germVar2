#!/usr/bin/env python
# 
###################################################################

#override the snpEff EFF fields in both header and info, split the fields and add them in INFO for easier conversion to table

###################################################################

import sys
import re
import vcf
from vcf.parser import _Info as VcfInfo

if __name__ == '__main__':
 
  vcf_reader = vcf.Reader(sys.stdin)
  
  vcf_reader.infos['EFF'] = VcfInfo('EFF', 1, 'String', 'Effect of mutation')
  vcf_reader.infos['Impact'] = VcfInfo('Impact', 1, 'String', 'Likely impact of mutation')
  vcf_reader.infos['FunClass'] = VcfInfo('FunClass', 1, 'String', 'Class')
  vcf_reader.infos['CodonChange'] = VcfInfo('CodonChange', 1, 'String', 'Nucleotide Change')
  vcf_reader.infos['AAChange'] = VcfInfo('AAChange', 1, 'String', 'Protein Change')
  #vcf_reader.infos['AAChange.p'] = VcfInfo('AAChange.p', 1, 'String', 'Protein Change')
  #vcf_reader.infos['AAChange.c'] = VcfInfo('AAChange.c', 1, 'String', 'Protein Change')
  vcf_reader.infos['AALength'] = VcfInfo('AALength', 1, 'Integer', 'Protein Length')
  vcf_reader.infos['Gene'] = VcfInfo('Gene', 1, 'String', 'Gene')
  vcf_reader.infos['BioType'] = VcfInfo('BioType', 1, 'String', 'BioType')
  vcf_reader.infos['Coding'] = VcfInfo('Coding', 1, 'String', 'Coding')
  vcf_reader.infos['Transcript'] = VcfInfo('Transcript', 1, 'String', 'Transcript')
  vcf_reader.infos['ExonRank'] = VcfInfo('ExonRank', 1, 'Integer', 'ExonRank')
  vcf_reader.infos['GTNum'] = VcfInfo('GTNum', 1, 'Integer', 'For which alt allele this is for')
  vcf_reader.infos['Warning'] = VcfInfo('Warning', 1, 'String', 'Warning')
  vcf_reader.infos['RPA'] = VcfInfo('RPA', 1, 'Integer', 'Times of tandem repeat')
  vcf_reader.infos['LOF_Gene'] = VcfInfo('LOF_Gene', 1, 'String', 'LOF gene')
  vcf_reader.infos['LOF_NT'] = VcfInfo('LOF_NT', 1, 'Integer', 'Number of transcripts')
  vcf_reader.infos['LOF_PT'] = VcfInfo('LOF_PT', 1, 'Float', 'Percentage of transcripts affected')
  vcf_reader.infos['NMD_Gene'] = VcfInfo('NMD_Gene', 1, 'String', 'LOF gene')
  vcf_reader.infos['NMD_N_Transcripts'] = VcfInfo('NMD_N_Transcripts', 1, 'Integer', 'Number of transcripts')
  vcf_reader.infos['NMD_P_Transcripts'] = VcfInfo('NMD_P_Transcripts', 1, 'Float', 'Percentage of transcripts affected')
  
  EFFkeys=['EFF','Impact','FunClass','CodonChange','AAChange','AALength','Gene','BioType','Coding','Transcript','ExonRank','GTNum','Warning']
  writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')
  
  for Record in vcf_reader:
    #split the snpEff field
    if Record.INFO.get('EFF', False):
      snpEff = Record.INFO['EFF'].rstrip(")").replace("(", "|").split("|")
      for i in range(len(snpEff)):
        if not snpEff[i] == '':
          Record.INFO[EFFkeys[i]] = snpEff[i]
      #if Record.INFO.get('AAChange', False):
       #   print Record.INFO['AAChange']
       #   Record.INFO['AAChange.p'] = Record.INFO['AAChange'].split('/')[0][2:]
       #   Record.INFO['AAChange.c'] = Record.INFO['AAChange'].split('/')[1][2:]
            

    if Record.INFO.get('LOF', False):
      LOF = Record.INFO['LOF'][0].rstrip(")").lstrip("(").split("|")
      Record.INFO['LOF_Gene'] = LOF[0]
      Record.INFO['LOF_NT'] = LOF[2]
      Record.INFO['LOF_PT'] = LOF[3]
      Record.INFO['LOF'] = None
    
    if Record.INFO.get('NMD', False):
      NMD = Record.INFO['NMD'][0].rstrip(")").lstrip("(").split("|")
      Record.INFO['NMD_Gene'] = NMD[0]
      Record.INFO['NMD_NT'] = NMD[2]
      Record.INFO['NMD_PT'] = NMD[3]
      Record.INFO['NMD'] = None
  
  
    writer.write_record(Record)




