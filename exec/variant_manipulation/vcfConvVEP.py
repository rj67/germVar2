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
  
  vcf_reader.infos['Allele'] = VcfInfo('Allele', 1, 'String', 'variant allele')
  vcf_reader.infos['ENSG'] = VcfInfo('ENSG', 1, 'String', 'Ensembl Gene ID')
  vcf_reader.infos['Feature'] = VcfInfo('Feature', 1, 'String', 'Ensembl Transcript')
  vcf_reader.infos['Feature_type'] = VcfInfo('Feature', 1, 'String', 'Feature type')
  vcf_reader.infos['Consequence'] = VcfInfo('Consequence', 1, 'String', 'Functional effect')
  vcf_reader.infos['cDNA_position'] = VcfInfo('cDNA_position', 1, 'String', 'cDNA position')
  vcf_reader.infos['CDS_position'] = VcfInfo('CDS_position', 1, 'String', 'CDS position')
  vcf_reader.infos['Protein_position'] = VcfInfo('Protein_position', 1, 'String', 'Protein position')
  vcf_reader.infos['Amino_acids'] = VcfInfo('Amino_acids', 1, 'String', 'Amino acid change')
  vcf_reader.infos['Codons'] = VcfInfo('Codons', 1, 'String', 'Codon change')
  vcf_reader.infos['DISTANCE'] = VcfInfo('DISTANCE', 1, 'Integer', 'distance')
  vcf_reader.infos['STRAND'] = VcfInfo('STRAND', 1, 'String', 'strand')
  vcf_reader.infos['SYMBOL'] = VcfInfo('SYMBOL', 1, 'String', 'Gene Symbol')
  #vcf_reader.infos['SYMBOL_SOURCE'] = VcfInfo('SYMBOL_SOURCE', 1, 'String', 'Symbol source')
  vcf_reader.infos['HGNC_ID'] = VcfInfo('HGNC_ID', 1, 'String', 'HGNC ID')
  vcf_reader.infos['BIOTYPE'] = VcfInfo('BIOTYPE', 1, 'String', 'BIOTYPE')
  vcf_reader.infos['CANONICAL'] = VcfInfo('CANONICAL', 1, 'String', 'Whether canonical transcript')
  vcf_reader.infos['CCDS'] = VcfInfo('CCDS', 1, 'String', 'CCDS ID')
  vcf_reader.infos['ENSP'] = VcfInfo('ENSP', 1, 'String', 'ENSP')
  vcf_reader.infos['SIFT'] = VcfInfo('SIFT', 1, 'String', 'SIFT prediction')
  vcf_reader.infos['PolyPhen'] = VcfInfo('PolyPhen', 1, 'String', 'PolyPhen prediction')
  vcf_reader.infos['EXON'] = VcfInfo('EXON', 1, 'String', 'EXON')
  vcf_reader.infos['INTRON'] = VcfInfo('INTRON', 1, 'String', 'INTRON')
  vcf_reader.infos['DOMAINS'] = VcfInfo('DOMAINS', 1, 'String', 'DOMAINS')
  vcf_reader.infos['HGVSc'] = VcfInfo('HGVSc', 1, 'String', 'HGVSc')
  vcf_reader.infos['HGVSp'] = VcfInfo('HGVSp', 1, 'String', 'HGVSp')
  vcf_reader.infos['CLIN_SIG'] = VcfInfo('CLIN_SIG', 1, 'String', 'CLIN_SIG')
  vcf_reader.infos['PUBMED'] = VcfInfo('PUBMED', 1, 'String', 'PUBMED')
  vcf_reader.infos['LoF_info'] = VcfInfo('LoF_info', 1, 'String', 'LoF')
  vcf_reader.infos['LoF_flags'] = VcfInfo('LoF_flags', 1, 'String', 'LoF')
  vcf_reader.infos['LoF_filter'] = VcfInfo('LoF_filter', 1, 'String', 'LoF')
  vcf_reader.infos['LoF'] = VcfInfo('LoF', 1, 'String', 'LoF')
  
  # keep these entries
  CSQ_Keys = [ 'Allele','ENSG','Feature','Feature_type','Consequence','cDNA_position','CDS_position','Protein_position','Amino_acids','Codons',
              'DISTANCE','STRAND','SYMBOL','HGNC_ID', 'BIOTYPE','CANONICAL','CCDS','ENSP','SIFT','PolyPhen','EXON','INTRON','DOMAINS','HGVSc','HGVSp',
              'CLIN_SIG','PUBMED','LoF_info','LoF_flags','LoF_filter','LoF' ]

  # all the entries present in the CSQ field
  ALL_Keys = vcf_reader.infos['CSQ'].desc.split("Format: ")[1].split('|')
  ALL_Keys = [w.replace('Gene', 'ENSG') for w in ALL_Keys]  

  writer = vcf.Writer(sys.stdout, vcf_reader, lineterminator='\n')

  for Record in vcf_reader:
    #split the snpEff field
    if Record.INFO.get('CSQ', False):
      CSQs = Record.INFO['CSQ']
      del Record.INFO['CSQ']
      for entry in CSQs: 
        veps = entry.split("|")
        for i in range(len(veps)):
          if not veps[i] == '':
            if ALL_Keys[i] in CSQ_Keys:
              Record.INFO[ALL_Keys[i]] = veps[i]
        writer.write_record(Record)
    else:
      writer.write_record(Record)
