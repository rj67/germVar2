#!/usr/bin/env python

import sys
import os
from sets import Set
import pandas as pd
import hashlib
import argparse
import vcf
from vcf.parser import _Info as VcfInfo
from math import isnan

######################################################################################################
def main() :
  

  bam_dict_file='all_bam_uid_SM_tmp.list'

  parser = argparse.ArgumentParser(description='fp filter')
  parser.add_argument('--input','-i', required=True, help="callset input file")
  parser.add_argument('--output','-o', required=True, help="callset output prefix")
  args = parser.parse_args()
  
  callset_file=args.input
  out_prefix=args.output

  ## input stuff
  # read in the os.systemset inp file
  callset_inp = pd.read_csv(callset_file, header=0, index_col=None, sep='\t')
  #print os.systemset_inp
  callset_inp['CHROM'] = callset_inp['CHROM'].astype(str)
  #os.systemset_inp['POS'] = callset_inp['POS'].astype(str)
  
  # read in Bam dictionary file that map sample ID to BAM file path
  bam_df = pd.read_csv(bam_dict_file, header=None, index_col=None, delim_whitespace=True)
  bam_df.columns = ['Patient', 'analysis', 'SAMPLE', 'bam_file']

  # merge os.systemset 
  callset_inp = pd.merge(callset_inp, bam_df, on="SAMPLE")

  # loop over var_uid
  GT_df = []
  VAR_df = []
  for name, group in callset_inp.groupby('var_uid'):
    print name
    CHROM = list(set(group['CHROM']))[0]
    POS = list(set(group['POS']))[0]
    REF = list(set(group['REF']))[0]
    ALT = list(set(group['ALT']))[0]
    tmp_dir = './tmp_' + hashlib.md5(name).hexdigest() 
    os.system('mkdir '+ tmp_dir)

    # write the bam list
    bamlist = tmp_dir + '/bam_list.list'
    # only interrogate germline or also somatic
    if True : 
      all_patients = group['Patient']
      all_rel = bam_df.query( "Patient in all_patients")
      all_rel['bam_file'].to_csv(bamlist, index= None, header=None)
    else:
      group['bam_file'].to_csv(bamlist, index= None, header=None)
    
    ## write the bed file
    bedfile = tmp_dir + '/' + name + '.bed'
    f1 = open(bedfile, 'w')
    #add POS by 1 if deletion
    #if len(ALT) < len(REF) :
      #f1.write('\t'.join([CHROM, str(POS+1), str(POS+1)])+'\n')
    #  f1.write('\t'.join([CHROM, str(POS), str(POS+1)])+'\n')
    #else:
    f1.write('\t'.join([CHROM, str(POS-1), str(POS)])+'\n')
    f1.close()
    print 'bam_list='+ bamlist + ' bed_file=' + bedfile + ' out_dir='+ tmp_dir+ ' project=' + name +' haplotypeCaller_BAM.sh'
    os.system('bam_list='+ bamlist + ' bed_file=' + bedfile + ' out_dir='+ tmp_dir+ ' project=' + name +' haplotypeCaller_BAM.sh')
    
    if os.path.getsize(tmp_dir + '/' + name + '.split.vcf') > 0:
      vcf_reader = vcf.Reader(open(tmp_dir + '/' + name + '.split.vcf', 'r'))
      for Record in vcf_reader:
        if Record.REF == REF and Record.ALT[0].sequence == ALT and Record.POS == POS :
          print Record.INFO
          Record_copy = Record.INFO.copy()
          Record_copy['var_uid'] = name
          Record_copy['QUAL'] = Record.QUAL
          VAR_df.append(Record_copy)
          # record sample info
          for sample in Record.samples:
            GT_df.append({ "var_uid":name, "SAMPLE":sample.sample, "GT":sample['GT'], "AD": sample['AD']})
        
  GT_df = pd.DataFrame(GT_df, columns=['var_uid', 'SAMPLE', 'GT', 'AD'])
  VAR_df = pd.DataFrame(VAR_df)
  VAR_df['AC'] = map(lambda x: int(x[0]), VAR_df['AC'])
  VAR_df['MLEAC'] = map(lambda x: int(x[0]), VAR_df['MLEAC'])
  VAR_df['AF'] = map(lambda x: float(x[0]), VAR_df['AF'])
  VAR_df['MLEAF'] = map(lambda x: float(x[0]), VAR_df['MLEAF'])
  VAR_df['VARTYPE'] = map(lambda x: str(x[0]), VAR_df['VARTYPE'])
  VAR_df['length'] = map(lambda x: int(x[0]), VAR_df['length'])
  VAR_df = VAR_df.drop('length.alt', 1)
  VAR_df = VAR_df.drop('length.ref', 1)
  if 'ALT_idx' in VAR_df.columns.values:
    VAR_df['ALT_idx'] = map(lambda x: x if isinstance(x, float) else x[0], VAR_df['ALT_idx'])
  
  GT_df['AD'] = map(lambda x: ','.join(map(str, x)) if x else x, GT_df['AD'])
  
  
  GT_df.to_csv(out_prefix+'.GT.tsv', sep='\t', index =None)
  VAR_df.to_csv(out_prefix+'.VAR.tsv', sep='\t', index = None)



if __name__ == "__main__":
    main()
