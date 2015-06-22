#' Select info from SNP df  
#'
#' select relevant infor mation from SNP df object
#' @param data SNP variant df
#' @param show Whether to view the df Defaults to TRUE.


showSNP <- function(data, show=T){
  cols <- c("Gene", "AAChange.s", "AC2", "TAC2", "pred_patho", "dele", "Clinvar", "RCVaccession", "OtherIDs", "ESP_AC", "X2kG_AC","ExAC_AdjAC", "cosm_acount", "cosm_scount", "ma_pred", "PHRED")
  if(show){
    View(data[colnames(df) %in% cols])
  }else{
    return(data[colnames(df) %in% cols])
  }
}