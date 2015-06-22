#!/usr/bin/env python

###################################################################

#vcfTrimMNP: trim common nucleotides in MNP, adjust POS accordingly, 

# some MNP especially from COSMIC  are actually SNPs, need to trim both ends.
# some MNP have trailing common nucleotides, only trim end

###################################################################

import vcf
import sys
from vcf.model import _Record as VcfRecord
from vcf.parser import _Info as VcfInfo
from vcf.model import _Substitution as VcfSubstitution

if __name__ == '__main__':

  vcf_reader = vcf.Reader(sys.stdin)
  
  writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')
  
  for Record in vcf_reader:
  
    # rely on SnpSift VARTYPE annotation
    # check for MNP flag is set and VARTYPE is SNP
    if Record.INFO.get('MNP', False) :
      if "SNP" in Record.INFO['VARTYPE'] :
        # figure out which position is different
        diff_pos = [i for i in  range(len(Record.REF)) if Record.REF[i] != Record.ALT[0].sequence[i] ]
        
        # check if more than one position differ
        if len(diff_pos) != 1 :
          #raise NameError('variant with MNP flag and VARTYPE=SNP have more than 1 base different')
          # keep up to the last different position, no need to change Position
          keeper = max(diff_pos)
          Records.REF = Record.REF[0:keeper+1] 
          Record.ALT[0].sequence = Record.ALT[0].sequence[0:diff_pos[0]+1]
        else :
          Record.REF = Record.REF[diff_pos[0]]
          Record.ALT[0].sequence = Record.ALT[0].sequence[diff_pos[0]]
          Record.POS = Record.POS + diff_pos[0]

    writer.write_record(Record)
  
