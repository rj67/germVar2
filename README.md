germVar2
=============

Supplementary materials for 
#### Pan-cancer sequencing analysis reveals frequent germline mutations in cancer genes 
Ruomu Jiang, William Lee, Nadeem Riaz, Chris Sander, Timothy J Mitchison^*, Debora S Marks^*

Install
-----------
    install.packages("devtools")
    library(devtools)
    install_github("rj67/germVar2")

Data objects
-----------
Dataframes that can be loaded

* list_goi -- candidate gene list

|    |Gene  |Approved.Name                |Ensembl.Gene    |MDG  |CPG  |Class |
|:---|:-----|:----------------------------|:---------------|:----|:----|:-----|
|83  |ATM   |ATM serine/threonine kinase  |ENSG00000149311 |TRUE |TRUE |H-TSG |
|135 |BRCA1 |breast cancer 1, early onset |ENSG00000012048 |TRUE |TRUE |H-TSG |

* all_patients -- all the patient information

|Patient |disease2 | age|       agez|EA   |race2 |gender |
|:-------|:--------|---:|----------:|:----|:-----|:------|
|P6-A5OG |ACC      |  45| -0.2248333|TRUE |WHITE |FEMALE |
|OR-A5JY |ACC      |  68|  1.0679583|TRUE |WHITE |FEMALE |

* LoF_vars -- variant information, each row is a variant and columns are various annotation

|     |Gene  |uid              |EFF                | TAC2|   AN2|rare |AAChange               |Transcript      |
|:----|:-----|:----------------|:------------------|----:|-----:|:----|:----------------------|:---------------|
|3444 |BRCA1 |17-41199682-C-T  |stop_gained        |    1| 17630|TRUE |p.Trp711*/c.2133G>A    |ENST00000491747 |
|3445 |BRCA1 |17-41201208-TG-T |frameshift_variant |    1| 17630|TRUE |p.Gln1732fs/c.5194delC |ENST00000493795 |

* LoF_muts -- variant carrier information, each row corresponds to the carrier of a particular variant.

|    |Gene  |uid              |Patient |disease2 |AAChange               | DP|        AB|N_hom | nA| nB|
|:---|:-----|:----------------|:-------|:--------|:----------------------|--:|---------:|:-----|--:|--:|
|8   |BRCA1 |17-41247941-T-G  |04-1336 |OV       |c.453A>C               | 39| 0.9411765|FALSE |  3|  0|
|205 |BRCA1 |17-41201208-TG-T |09-2045 |OV       |p.Gln1732fs/c.5194delC | 96| 0.8541667|FALSE |  1|  0|

*  nsSNP_vars -- variant information, each row is a variant and columns are various annotation

|                |Gene  |uid             |EFF              | TAC2|   AN2|rare |AAChange               |Transcript      |dele  |RCVaccession              | cosm_scount|
|:---------------|:-----|:---------------|:----------------|----:|-----:|:----|:----------------------|:---------------|:-----|:-------------------------|-----------:|
|17-41201181-C-A |BRCA1 |17-41201181-C-A |missense_variant |    1| 17630|TRUE |p.Gly1788Val/c.5363G>T |ENST00000357654 |TRUE  |RCV000048961;RCV000031241 |          NA|
|17-41215920-G-A |BRCA1 |17-41215920-G-A |missense_variant |    1| 17630|TRUE |p.Ala1708Val/c.5123C>T |ENST00000357654 |FALSE |NA                        |          NA|

* nsSNP_muts -- variant carrier information, each row corresponds to the carrier of a particular variant.

|   |Gene  |uid             |Patient |disease2 |AAChange              |  DP|        AB|N_hom | nA| nB|
|:--|:-----|:---------------|:-------|:--------|:---------------------|---:|---------:|:-----|--:|--:|
|3  |BRCA1 |17-41245027-G-A |02-0047 |GBM      |p.Arg841Trp/c.2521C>T | 330| 0.4575758|FALSE |  1|  1|
|89 |BRCA1 |17-41245027-G-A |05-5425 |LUAD     |p.Arg841Trp/c.2521C>T | 195| 0.5179487|FALSE |  3|  1|




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
