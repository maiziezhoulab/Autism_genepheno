# Autism_GenePheno

 ### Go through the cells of Jupyter Notebook 'Gene_Phenotype_Extraction.ipynb'.
 
 The final cell will run the function which starts to output the results at the beginning or at where you stopped last time.
 
 ##### Note that the `get_input_dirs` function in the first cell lists the directories of input files. 
 
 ```
#============================================================================================
ASDPTO_dir = './Phenotype_list/ASDPTO.csv'             # The ASDPTO part phenotype list.
UMLS_dir = './Phenotype_list/UMLS.txt'                 # The UMLS part phenotype list.
HPOdel_dir = './Phenotype_list/del_ls_HPOtreeview.txt' # Removed upper-level concepts in HPO.
HPOtreeview_dir = './Phenotype_list/HPO(treeview).txt' # The treeview form of HPO list.
c2upper_dir = './Phenotype_list/c2upper.txt'           # Phenotypes and their upper-level concepts.
allGene_dir = './Genotype_list/export_latest.tsv'      # The genotype list.
papers_dir = './XML_datasets_5year/'                   # Target papers in the last five years.
#============================================================================================
```
Please make sure they are in the same format as ours if you want to use your own input files or change their respective reading directories if you want to put the input files arbitrarily.


##### Outputs will be presented in three directories named 'Extraced_results', 'Sum_for_each_paper' and 'Sum_all'.
In 'Extraced_results', the extracted information of those papers which get at least one extracted sentences is noted down as Json files, named after the PMCid of the papers. The format should be as follows:

 ```
{
    "PMCid": "PMC6571119", 
    "Title": "Impaired neurodevelopmental pathways in autism spectrum disorder: a review of signaling mechanisms and crosstalk (Published on 6/15/2019)", 
    "Sentences": {
        "Sentence0": {
            "Content": "For instance, Neuroligins (NLGN), fragile X mental retardation 1 (FMR1), ubiquitin-protein ligase E3A (UBE3A), and DLX, which modulate BMP signaling, have been found to be associated with ASD [10–13].", 
            "Gene": [
                "FMR1", 
                "UBE3A"
            ], 
            "Original phenotype": [
                "mental retardation"
            ], 
            "Normolized phenotype": [
                [
                    "C0025362", 
                    "Mental retardation", 
                    "OMIM, HPO, SNOMEDCT_US", 
                    "HP:0001249"
                ]
            ], 
            "Upper level concepts (HPO only)": [
                "Abnormality of the nervous system"
            ]
        }
        ...
    }
}

```

In 'Sum_for_each_paper', each Json file saves n_g (occured genotypes and the times they occured) and n_p (occured phenotypes and the times they occured) for the respective paper. The format should be as follows:


 ```
{
    "PMCid": "PMC6741850", 
    "Only abstract?": "N", 
    "Number of Sentences": 40, 
    "n_g": {
        "TRPM8": 1, 
        "FMR1": 2, 
        "MB": 1, 
        "PTEN": 1
    }, 
    "n_p": {
        "['C0009443', '(Acute nasopharyngitis or rhinitis) or (common cold)', 'SNOMEDCT_US', 'NULL']": 1, 
        "['C0456909', 'Blindness', 'MSH, OMIM, SNOMEDCT_US, HPO', 'HP:0000618']": 1, 
        "['C0233577', 'Mimicry', 'SNOMEDCT_US', 'NULL']": 1
    }
}

```

In 'Sum_all', the overall n_g and n_p of 5-years papers are given in 'n_g.txt' and 'n_p.txt'; Other general information are given in 'In_Summary.txt' and the format of it should be as follows:


 ```
Number of paper processed: 15095

Number of the articles have only abstract: 5008

Number of paper get at least one sentence: 8512

Sentences extracted: 62183

N_tot =  2754875

Unique gene list from all papers: ['PTPRE', 'TSPO', ...]

Unique normalized phenotype list from all papers: ["['C1510472', 'Dependence syndrome', 'SNOMEDCT_US', 'NULL']", "['C0008372', 'Intrahepatic cholestasis', 'OMIM, HPO, SNOMEDCT_US', 'HP:0001406']", ...]

```

