germVar2
=============

Supplementary materials for 
#### Pan-cancer sequencing analysis reveals frequent germline mutations in cancer genes 
Ruomu Jiang, William Lee, Nadeem Riaz, Chris Sander, Timothy J Mitchison*, Debora S Marks*

Install
-----------
    install.packages("devtools")
    library(devtools)
    install_github("rj67/germVar2")

Data objects
-----------
Dataframes that can be loaded

* list_goi -- candidate gene list
|Gene |Approved.Name    |Ensembl.Gene    |MDG   |CPG   |Class       |
|:----|:----------------|:---------------|:-----|:-----|:-----------|
|ABI1 |abl-interactor 1 |ENSG00000136754 |FALSE |FALSE |Other       |
|ABI2 |abl-interactor 2 |ENSG00000138443 |FALSE |FALSE |PutativeTSG |

* all_patients -- all the patient information
* LoF_vars, nsSNP_vars -- variant information, each row is a variant and columns are various annotation
* LoF_muts, nsSNP_muts -- variant carrier information, each row corresponds to the carrier of a particular variant.

Juptyer notebooks
-----------
Reproduce most of the analysis/figures in the paper

* project_overview -- Samples, candidate gene, all variants overview.
* known_cancer_gene_variants -- Summary variants in known cancer genes.
* loss_of_heterozygousity_analysis -- LOH of all germline variants
* low_frequency_variants_association -- Assocation test of low frequency missense and truncation variants comparing to 1000G and ESP

Convenience functions
-----------

* plotMutRNASeq -- Plot mutation RNASeq levels 
* plotDiseaseDistr -- Plot cancer type distribution given a list of mutations

Dependency
-----------

* plyr, dplyr, reshape2, ggplot2, magrittr, RColorbrewer, gridExtra
