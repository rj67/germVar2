#!/usr/bin/env python

import vcf
import sys
from vcf.parser import _Info as VcfInfo

vcf_reader = vcf.Reader(sys.stdin)

vcf_reader.infos['ALT_idx'] = VcfInfo( 'ALT_idx', 'A', 'String', 'index for the alternative alleles')
vcf_reader.infos['ALT_pos'] = VcfInfo( 'ALT_pos', 1, 'String', 'original postition for the multiallele complex')
vcf_reader.infos['ALT_num'] = VcfInfo( 'ALT_num', 1, 'Integer', 'number of alternative allele for the multiallele complex')
vcf_reader.infos['ALTs_orig'] = VcfInfo( 'ALTs_orig', 1, 'String', 'all original ALTs')
vcf_reader.infos['REF_orig'] = VcfInfo( 'REF_orig', 1, 'String', 'original REF')
vcf_reader.infos['ACs_orig'] = VcfInfo( 'ACs_orig', 1, 'String', 'all original ACs')

writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')

# info field that might be multi-allelic
for Record in vcf_reader:

  # when encountering multiallele, annotate alt sequence
  if len(Record.ALT) > 1 :

    ALT_idx = ','.join([ str(x) for x in range(1, len(Record.ALT)+ 1)])
    ALT_pos = str(Record.CHROM) + ':' + str(Record.POS)
    ALT_num = str(len(Record.ALT))
    ALTs_orig = '|'.join([ x.sequence for x in Record.ALT])
    REF_orig = Record.REF
    if Record.INFO.get('AC', False):
      ACs_orig = '|'.join([ str(x) for x in Record.INFO['AC']])

    Record.add_info('ALT_idx',ALT_idx)
    Record.add_info('ALT_pos',ALT_pos)
    Record.add_info('ALT_num',ALT_num)
    Record.add_info('ALTs_orig',ALTs_orig)
    Record.add_info('REF_orig',REF_orig)
    if Record.INFO.get('AC', False):
      Record.add_info('ACs_orig',ACs_orig)
    writer.write_record(Record)

  # otherwise, use Pyvcf to print line
  else:
    writer.write_record(Record)

