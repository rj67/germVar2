#!/usr/bin/env python

###################################################################

#vcfAnnoPfam: annotate pfam domain information according to SnpEff annotation

###################################################################

import sys
import re
import vcf
import argparse
from vcf.parser import _Info as VcfInfo

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=' vcfAnnoPfam')
  parser.add_argument('--pfam','-p',
                    required=True,
                    help="Pfam data base file")
  
  args = parser.parse_args()

  all_entries = []
  lines = open(args.pfam, 'r').readlines()
  for line in lines[1:]:
    fields = line.split(' ')
    all_entries.append(fields)
  
  # initialize pfam_dict
  pfam_dict = {}
  for entry in all_entries:
    pfam_dict[entry[1]] = []
  
  # put each entry into the slot
  for entry in all_entries:
    pfam_dict[entry[1]].append((int(entry[4]),int(entry[5]),entry[3],entry[7])) 
    
  vcf_reader = vcf.Reader(sys.stdin)
  
  vcf_reader.infos['AA_pos'] = VcfInfo( 'AA_pos', 1, 'Integer', 'Amino acid change position')
  vcf_reader.infos['Pfam'] = VcfInfo( 'Pfam', 0, 'Flag', 'whether Gene in pfam')
  vcf_reader.infos['InDom'] = VcfInfo( 'InDom', 0, 'Flag', 'whether in pfam domain')
  vcf_reader.infos['PfamDom'] = VcfInfo( 'PfamDom', 1, 'String', 'info of pfam domain')
  vcf_reader.infos['AftDom'] = VcfInfo( 'AftDom', 0, 'Flag', 'whether after pfam domain')
  
  writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')
  
  numera = re.compile('[0-9]+')
  for Record in vcf_reader:
    # if coding change
    if Record.INFO.get('AAChange', False) :
      
      # get the amino acid change position
      AA_pos = int(numera.findall(Record.INFO.get('AAChange'))[0])
      
      # special condition where MNP and nonsynonymous change affect two residues, only second residue cahnges
      if "MNP" in Record.INFO['VARTYPE'] and Record.INFO['EFF'] == "NON_SYNONYMOUS_CODING" :
        AAs = Record.INFO['AAChange'].split(str(AA_pos)) 
        if len(AAs[0]) != len(AAs[1]) :
          raise NameError('MNP nonsynoymous variants affect unequal residues in AAChange')
        elif len(AAs[0]) > 1 :
          diff_pos = [i for i in  range(len(AAs[0])) if AAs[0][i] != AAs[1][i] ]
          AA_pos += min(diff_pos)

      Record.add_info('AA_pos',AA_pos)
  
      # if gene has domain in Pfam
      if pfam_dict.get(Record.INFO['Gene'], False):
  
        Record.add_info('Pfam',True)
  
        # loop through each pfam match
        far_end = []
        for match in pfam_dict.get(Record.INFO['Gene']):
          far_end.append(match[1])
          
          # figure out whether AA in a domin
          if (AA_pos >= match[0]) & (AA_pos <=match[1]):
            
            Record.add_info('InDom',True)
            Record.add_info('PfamDom',match[2]+'|'+match[3])
  
        # see if AA is after the farthest domain
        if AA_pos > max(far_end) :
          Record.add_info('AftDom',True)
  
    writer.write_record(Record)

