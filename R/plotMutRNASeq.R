#' Plot mutation RNASeq levels 
#'
#' Plot the all_mRNA levels of patients with variants in a specific gene
#' @param df Supplied mutation df or a list of patients  Defaults to TRUE.
#' @param Gene Which gene to plot Defaults to NA.
#' @param transformed Whether to plot variance-stablized counts Defaults to TRUE.
#' @keywords RNASeq

plotMutRNASeq <- function(data, Gene=NA, transformed = T){
  library(RColorBrewer)
  # figure out which gene to plot if not supplied
  if (is.na(Gene)){
    Gene =  unique(data$Gene)
    if(is.na(Gene)) stop("No gene specified")
  }
  # get RNASeq data
  all_mRNA <- getRNASeq(Gene)
  # figure out the patients, whether supplied is a character list or a mutation df
  if(is.null(dim(data))){
    Patients <- data
  } else {
    Patients <- data[["Patient"]]
    if(all(is.na(Patients))) stop("No patients specified")
  }
  # drop diseases with no variant
  all_mRNA <- droplevels(subset(all_mRNA, disease %in% droplevels(subset(all_mRNA, Patient %in% Patients))$disease))
  if(transformed){
    p <- ggplot(aes(reorder(disease, ihs_count, median), ihs_count), data = all_mRNA) + geom_boxplot(outlier.shape = NA)
    p <- p  + ylab("ihs_count")
  }else{
    p <- ggplot(aes(reorder(disease, normalized_count, median), normalized_count), data = all_mRNA) + geom_boxplot(outlier.shape = NA)
    p <- p  + ylab("normalized_count")
  }
  p <- p + geom_jitter(aes(color=disease), data = subset(all_mRNA, Patient %in% Patients))
  p <- p + theme_few() + theme(axis.text.x=element_text(angle=45, hjust=1)) + labs(x=NULL)
  p <- p + scale_color_manual(values=colorRampPalette(brewer.pal(8, "Set1"))(length(unique(all_mRNA$disease))), guide="none")
  labelDisease(p)
}