#' Plot mutation disease types 
#'
#' Plot the cancer type distribution of supplied patient list
#' @param data Supplied mutation data or a list of patients  Defaults to TRUE.
#' @param Gene Which gene to plot Defaults to NA.
#' @param transformed Whether to plot variance-stablized counts Defaults to TRUE.
#' @keywords RNASeq

plotDiseaseDistr <- function(data, ){
  gender_color <- c("#e31a1c", "#1f78b4")
  # figure out the patients 
  Patients <- extractPatient(data)
  
  to_plot <- subset(all_tcga, !duplicated(disease2)[c("disease2", "study_size", "femme_ratio")]
  to_plot$expected_F <- to_plot$study_size * to_plot$femme_ratio * length(Patients) / sum(to_plot$study_size)
  to_plot$expected_M <- to_plot$study_size * (1-to_plot$femme_ratio) * length(Patients) / sum(to_plot$study_size)
  to_plot %<>% plyr::join(., subset(all_tcga, !duplicated(Patient))[c("Patient", "disease2", "gender")] %>% subset(., Patient %in% Patients) %>% group_by(., disease2) %>% 
                            dplyr::summarise(., actual_size = length(Patient), actual_F = actual_size*sum(gender[!is.na(gender)]=="FEMALE")/length(gender[!is.na(gender)]),
                                             actual_M = actual_size - actual_F ))
  to_plot$actual_size <- replaZero(to_plot$actual_size)
  to_plot$actual_F <- replaZero(to_plot$actual_F)
  to_plot$actual_M <- replaZero(to_plot$actual_M)
  to_plot %<>% arrange(., -study_size) %<>% mutate(., disease2 = factor(disease2, levels=disease2))
  
  to_long <- reshape2::melt(to_plot[c("disease2", "expected_F", "expected_M", "actual_F", "actual_M")], id.var="disease2")
  to_long$actual <- to_long$variable %in% c("actual_F", "actual_M")
  p1 <- ggplot(to_plot, aes(disease2, value)) 
  p1 <- p1 + geom_bar(stat="identity", aes(color=variable), fill="white", alpha=1, width=0.9, data=subset(to_long, !actual)) 
  p1 <- p1 + geom_bar(stat = "identity", aes(fill=variable), data=subset(to_long, actual), alpha=1, width=0.45)
  p1 <- p1 + scale_fill_manual(values=gender_color, guide=guide_legend(title="Observed", keywidth=0.9, keyheight=0.9), labels=c("Female", "Male"))
  p1 <- p1 + scale_color_manual(values=gender_color, guide=guide_legend(title="Expected", keywidth=0.9, keyheight=0.9), labels=c("Female", "Male"))
  p1 <- p1 + theme_bw() + ylab("Number of patients") + xlab("") + theme(legend.position=c(0.9,0.6))
  p1 <- labelDisease(p1)
  p1 <- p1 + theme( panel.grid.major.x=element_blank())
  p1 <- p1 + theme(axis.text.x = element_text(angle = 45, hjust = 1, size=rel(.8)))
  
}