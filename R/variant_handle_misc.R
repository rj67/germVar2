#' Select info from SNP df  
#'
#' select relevant infor mation from SNP df object
#' @param data SNP variant df
#' @param show Whether to view the df Defaults to TRUE.


showSNP <- function(data, show=T){
  cols <- c("Gene", "AAChange.s", "EFF", "AC2", "TAC2", "AN2", "TEAC2", "EAN", "ESP_AC", "ESP_AN", "ESP_EA_AC", "ESP_EA_AN", "X2kG_AC", "ExAC_AdjAC", "rare",
            "pred_patho", "dele", "Clinvar", "RCVaccession", "cosm_acount", "cosm_scount", "ma_pred", "PHRED", "MDG", "CPG", "Class",
            "NALT_AD_med", "TALT_AD_med", "NAB_med", "TAB_med", "Transcript", "AAChange", "uid")
  #print(setdiff(cols, colnames(data)))
  if(show){
    View(data[cols])
  }else{
    return(data[cols])
  }
}


#' Select info from LoF df  
#'
#' select relevant infor mation from LoF df object
#' @param data LoF variant df
#' @param show Whether to view the df Defaults to TRUE.

showLoF <- function(data, show=T){
  cols <- c("Gene", "AAChange.p", "EFF", "AC2", "TAC2", "AN2", "TEAC2", "EAN", "ESP_AC", "ESP_AN", "ESP_EA_AC", "ESP_EA_AN", "X2kG_AC", "ExAC_AdjAC", "rare",
            "tier1", "tier2", "NMD_HC", "LoF_filter", "ExonRank", "TotalExon", "CDS_frac", "MDG", "CPG", "Class",
            "NALT_AD_med", "TALT_AD_med", "NAB_med", "TAB_med", "Transcript", "AAChange", "uid")
  
  #print(setdiff(cols, colnames(data)))
  if(show){
    View(data[cols])
  }else{
    return(data[cols])
  }
}


#' Select info from mutation df  
#'
#' select relevant infor mation from LoF df object
#' @param data mut df

showMut <- function(data){
  cols <- c("uid", "Patient","Gene", "event_uid", "AAChange", "EFF", "Class","disease2", "DP", "AB", "N_hom","agez", "gender")
  #print(setdiff(cols, colnames(data)))
  return(data[cols])
}