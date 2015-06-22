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
  
  vcf_reader.infos['AC'] = VcfInfo('AC', 1, 'Integer', 'Allele count in genotypes')
  vcf_reader.infos['AF'] = VcfInfo('AF', 1, 'Float', 'Allele Frequency')
  vcf_reader.infos['MLEAC'] = VcfInfo('MLEAC', 1, 'Integer', 'Maximum likelihood expectation (MLE) for the allele counts (not necessarily the same as the AC)')
  vcf_reader.infos['MLEAF'] = VcfInfo('MLEAF', 1, 'Float', 'Maximum likelihood expectation (MLE) for the allele frequency (not necessarily the same as the AF)')
  vcf_reader.infos['ALT_idx'] = VcfInfo('ALT_idx', 1, 'String', 'index for the alternative alleles')
  vcf_reader.infos['length'] = VcfInfo('length', 1, 'Integer', 'length(ALT) - length(REF) for each ALT')
  vcf_reader.infos['VARTYPE'] = VcfInfo('VARTYPE', 1, 'String', 'variant types')
  if vcf_reader.infos.get('CSQ', False):
    del vcf_reader.infos['CSQ'] 
  if vcf_reader.infos.get('LOF', False):
    del vcf_reader.infos['LOF'] 
  if vcf_reader.infos.get('NMD', False):
    del vcf_reader.infos['NMD'] 
  
  writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')
  for Record in vcf_reader:
    writer.write_record(Record)
