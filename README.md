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

|Patient |disease2 | age|       agez|EA   |race2 |gender |
|:-------|:--------|---:|----------:|:----|:-----|:------|
|P6-A5OG |ACC      |  45| -0.2248333|TRUE |WHITE |FEMALE |
|OR-A5JY |ACC      |  68|  1.0679583|TRUE |WHITE |FEMALE |

* LoF_vars, nsSNP_vars -- variant information, each row is a variant and columns are various annotation

|Gene     |uid            |EFF                | TAC2|   AN2|rare |AAChange             |Transcript      |
|:--------|:--------------|:------------------|----:|-----:|:----|:--------------------|:---------------|
|TNFRSF18 |1-1139268-G-A  |stop_gained        |    1| 16810|TRUE |p.Arg221*/c.661C>T   |ENST00000379265 |
|TNFRSF18 |1-1140761-AC-A |frameshift_variant |    1| 17208|TRUE |p.Val100fs/c.298delG |ENST00000379265 |

|              |Gene    |uid           |EFF              | TAC2|   AN2|rare |AAChange             |Transcript      |dele  |
|:-------------|:-------|:-------------|:----------------|----:|-----:|:----|:--------------------|:---------------|:-----|
|1-1149118-G-A |TNFRSF4 |1-1149118-G-A |missense_variant |    1| 16918|TRUE |p.Arg65Cys/c.193C>T  |ENST00000379236 |FALSE |
|1-3301758-A-G |PRDM16  |1-3301758-A-G |missense_variant |    3| 17614|TRUE |p.Asn161Asp/c.481A>G |ENST00000270722 |FALSE |

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
