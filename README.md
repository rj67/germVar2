germVar2
=============

TCGA cancer patient germline variants in a bunch of candidate genes 

Data objects
-------

* list_goi -- candidate gene list
* all_patients -- all the patient metadata
* LoF_var, nsSNP_var -- variant centric dataframe, containing all the truncation and missense variants, 
* LoF_mut, nsSNP_mut -- patient centric dataframe


Main functions
-----------

* plotMutRNASeq -- Plot mutation RNASeq levels 
* plotDiseaseDistr -- Plot cancer type distribution given a list of mutations



Dependency
-----------

* dplyr, reshape2, ggplot2, magrittr, RColorbrewer
