germVar2
=============

TCGA cancer patient germline variants in a bunch of candidate genes 

Data objects
-------

* list_goi -- candidate gene list
* all_patients -- all the patient metadata
* LoF_vars, nsSNP_vars -- variant centric dataframe, containing all the truncation and missense variants, 
* LoF_muts, nsSNP_muts -- patient centric dataframe

Main functions
-----------

* plotMutRNASeq -- Plot mutation RNASeq levels 
* plotDiseaseDistr -- Plot cancer type distribution given a list of mutations

Juptyer notebooks
-----------

* project_overview -- Samples, candidate gene, all variants overview.
* known_cancer_gene_variants -- Summary variants in known cancer genes.
* loss_of_heterozygousity_analysis -- LOH of all germline variants
* low_frequency_variants_association -- Assocation test of low frequency missense and truncation variants comparing to 1000G and ESP

Dependency
-----------

* plyr, dplyr, reshape2, ggplot2, magrittr, RColorbrewer, gridExtra
