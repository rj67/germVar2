#!/usr/bin/Rscript --vanilla --slave

# read in a vcf file, call vcf2tsv to convert it to table, read in the table save as RData

#print(commandArgs())
# check input is vcf file
vcf_filename <- commandArgs()[6]
if (substr(vcf_filename, nchar(vcf_filename)-2, nchar(vcf_filename)) != "vcf" ){
  stop("input filename doesn't end with vcf")
}
vcf_prefix <- substr(vcf_filename, 1, nchar(vcf_filename)-4) 
tsv_filename <- paste(vcf_prefix, ".table", sep="")

# convert vcf to tsv
vcf2tsv_call <- paste0(c("vcf2tsv -g -n \".\" ", vcf_filename, " | grep -v \"\\.\\/\\.\" > ", tsv_filename ), collapse="")
#vcf2tsv_call <- paste0(c("vcf2tsv -g -n \".\" ", vcf_filename, " > ", tsv_filename ), collapse="")
print(vcf2tsv_call)
system(vcf2tsv_call)

# read in tsv
call_set <- read.delim(tsv_filename, strip.white = T, na.string = ".", stringsAsFactors = F)
# remove the columns that are all NA
call_set <- call_set[colSums(is.na(call_set))<nrow(call_set)]
# remove the columns that are all 0
call_set <- call_set[colSums(call_set==0, na.rm=T)<nrow(call_set)]
# convert some columns to factors
#call_set$Gene <- factor(call_set$Gene)
#call_set$EFF <- factor(call_set$EFF)
#call_set$Impact <- factor(call_set$Impact)

out_filename <- paste(vcf_prefix, ".RData", sep="")

comment(call_set) <- vcf_prefix
#print("write to file")
#print(outname)
save( call_set, file=out_filename)

#call_set <- read.delim('/dev/stdin', header = T, sep='\t')
#print(call_set)
