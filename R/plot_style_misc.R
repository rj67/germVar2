#' Translate disease abbreviation
#'
#' Plot the all_mRNA levels of patients with variants in a specific gene
#' @param p ggplot2 object

labelDisease <- function(p, axis="x", ...){
  if(axis == "x"){
    p <- p + scale_x_discrete(..., labels = c( "BRCA"="Breast", 
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
  }else if(axis =="y"){
    p <- p + scale_y_discrete(..., labels = c( "BRCA"="Breast", 
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
  }
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
  return(unique(Patients))
}

#' Unify ggplot2 dimensions
#'
#' Make ggplot2 objects the same width and height
#' @param width unify width data Defaults to TRUE
#' @param height unify height Defaults to TRUE

unifyPlotDim <- function(pl, width = T, height = T){
  pl <- lapply(pl, ggplotGrob)
  widths <- do.call(unit.pmax, lapply(pl, "[[", "widths"))
  heights <- do.call(unit.pmax, lapply(pl, "[[", "heights"))
  if(width){
    pl <- lapply(pl, function(g) {g$widths <- widths; g})
  }
  if(height){
    pl <- lapply(pl, function(g) {g$heights <- heights; g})
  }
  return(pl)
}

#' Fill all combination of the two input columns
#'
#' Form the outer product of the input column X,Y, typically disease2, Gene
#' @param data input data
#' @param X column 1 Defaults to "disease2"
#' @param Y column 2 Defaults to "Gene"

expand_outer <- function(data, X = "disease2", Y = "Gene"){
  df <- data.frame(var1 = rep(unique(data[[X]]), times=length(unique(data[[Y]]))), 
                      var2 = rep(unique(data[[Y]]), each=length(unique(data[[X]])))) 
  colnames(df) <- c(X, Y)
  return(df)
}


#' Replace NAs with 0
#'
#' Take in vector, replace NAs, return vector
#' @param x input data

replaZero <- function(x){
  x[is.na(x)] <- 0
  return(x)
}

#' Label significance level for pvalues
#'
#' Take in pval vector, return character vector
#' @param pval input data

sigSymbol <- function(pval) {
  return(do.call(c, sapply(pval, function(x) ifelse(x>0.05, "", ifelse(x>0.01, "*", ifelse(x>0.001, "**", "***"))), simplify=F, USE.NAMES=F)))
}


#' manually adjust a few genes' plotting coordinate
#'
#' Assume the plotting dataframe contains plot_x, plot_y for coordiantes
#' @param df input plotting data
#' @param Genes input Gene list
#' @param axis which axis
#' @param nudge amount

nudgeXY <- function(df, Genes, axis, nudge){
  for( x in Genes) {
    if (axis == "x"){
      df$plot_x[df$Gene == x] <- df$plot_x[df$Gene == x] + nudge
    } else{
      df$plot_y[df$Gene == x] <- df$plot_y[df$Gene == x] + nudge
    }
  }
  return(df)
}
