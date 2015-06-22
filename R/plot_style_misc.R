#' Translate disease abbreviation
#'
#' Plot the all_mRNA levels of patients with variants in a specific gene
#' @param p ggplot2 object

labelDisease <- function(p){
  p <- p + scale_x_discrete(labels = c( "BRCA"="Breast", 
                                        "GBM"="Glioblastoma", 
                                        "LGG"="Glioma",
                                        "KICH"="Renal Chromophobe", 
                                        "KIRC"="Renal Clear Cell", 
                                        "KIRP"="Renal Papillary", 
                                        "LUAD" = "Lung Adeno-", 
                                        "UCEC"="Endometrial",
                                        "HNSC"="Head Neck", 
                                        "THCA"="Thyroid", 
                                        "OV"="Ovarian", 
                                        "SKCM"="Skin", 
                                        "COLO"="Colorectal", 
                                        "COAD"="Colon", 
                                        "READ"="Rectal", 
                                        "STAD"="Stomach", 
                                        "PRAD"="Prostate", 
                                        "BLCA"="Bladder", 
                                        "LIHC"="Liver", 
                                        "CESC"="Cervical",
                                        "SARC"="Sarcoma", 
                                        "PCPG"="Pheochromocytoma", 
                                        "ESCA"="Esophageal", 
                                        "ACC"="Adrenocortical", 
                                        "PAAD"="Pancreatic", 
                                        "UCS"="Uterine", 
                                        "LUSC"="Lung Squam-" ))
  return(p)
}

#' Extract patient names from input data
#'
#' input data maybe a vector or data frame
#' @param data input data

extractPatient <- function(data){
  if(is.null(dim(data))){
    Patients <- data
  } else {
    Patients <- data[["Patient"]]
    if(all(is.na(Patients))) stop("No patients specified")
  }
  return(Patients)
}