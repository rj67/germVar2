germVar2
=============

TCGA cancer patient germline variants in a bunch of candidate genes 

Data objects
-------

The following markups are supported.  The dependencies listed are required if
you wish to run the library. You can also run `script/bootstrap` to fetch them all.

* list_goi -- candidate gene list
* all_tcga -- all the sample metadata
* LoF_var, nsSNP_var -- all the truncation and missense variants, variant centric dataframe


Main functions
-----------

* plotMutRNASeq -- Plot mutation RNASeq levels 
* plotDiseaseDistr -- Plot cancer type distribution given a list of mutations



Dependency
-----------

* dplry, reshape2, ggplot2, magrittr, RColorbrewer
