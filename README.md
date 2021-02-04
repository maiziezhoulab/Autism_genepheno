# Autism_genepheno

 ### Step1: Go through the cells of Jupyter Notebook 'Autism_genepheno_step1.ipynb'.
 
 The final cell will run the function which starts to output the results at the beginning or at where you stopped last time.
 
 ##### Note that the `get_dirs` function in the first cell lists the directories of input and output files. 
 
 ```
#============================================================================================
ASDPTO_dir = './source/ASDPTO.csv'                     # The ASDPTO part phenotype list.
UMLS_dir = './source/UMLS.txt'                         # The UMLS part phenotype list.
allGene_dir = './source/export_latest.tsv'             # The genotype list.
papers_dir = './XML_datasets_5year/'                   # Target papers in the last five years.

out_dir = './Autism_genepheno_results/'                # default = './Autism_genepheno_results/'
#============================================================================================
```
The gene list sees ['export_latest.tsv'](https://drive.google.com/file/d/19suxgUE5VY0jrlY8kGoX3zyb_yHptgDi/view?usp=sharing).

Papers in the last 5 years see ['XML_datasets_5year'](https://drive.google.com/drive/folders/1431UFcXAqdx0lub2vSe28khxkSmt73__?usp=sharing).

Please make sure your input are in the same format as ours if you want to use your own or change their respective reading directories if you want to put the input files arbitrarily.


##### The default output directory named  named './Autism_genepheno_results/' is organized as follows:
```
Autism_genepheno_results
|-Extracted_results
|   |-PMCxxxxxxx.json
|   ...
|-Sum_for_each_paper
|    |-PMCxxxxxx.txt
|    ...
|-Sum_all
     |-n_g.txt
     |-n_p.txt
     |In_Summary.txt
```
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

 ### Step2: 'NPMI_calculate.ipynb'.
 
The second step is analyzing the result in the first step. This script will calculate the NPMI of each pair and also output the gene-phenotype matrix. 

The dir of the input file and output file is shown in the second cell of the script.

```
# input file dir
json_path = './Autism_genepheno_results/Extraced_results'              # the output file of step1
np_dir = './Autism_genepheno_results/Sum_all/n_p.txt'                  # the output file of step1
ng_dir = './Autism_genepheno_results/Sum_all/n_g.txt'                  # the output file of step1
In_Summary_dir='./Autism_genepheno_results/Sum_all/In_Summary.txt'     # the output file of step1
sfari_gene_dir='../source/SFARI-Gene_genes_12-11-2020release_12-19-2020export.xlsx'# the SFARI genes file dir

# output file dir
NPMI_result_dir='./Autism_genepheno_results/NPMI_file/'                # folder of NPMI file 
```

When finished, you will get:
```
Autism_genepheno_results
|-NPMI_file
    |-NPMI.json
    |-NPMI.csv
    |-NPMI_above_zero.csv
    |-graph_matrix_01_NPMIabove0.csv
```

The format of ‘NPMI.json’ file should be as follows:

```
[
    {
        "gene": "SHANK3",
        "phenotype": "['C1853490', '22q13 Deletion Syndrome', 'MSH', 'NULL']",
        "NPMI": 0.607088439701336,
        "gene_sfari_class": 1.0,
        "n_g": 1964,  # the number of sentences mentioning the gene
        "n_p": 256,   # the number of sentences mentioning the phenotype
        "n_gp": 94.0  # the number of sentences where the gene and phenotype co-occurs
    },
    ...
]
```

The format of ‘NPMI.csv’ file and ‘NPMI_above_zer.csv’ file should be as follows:

```
| gene   | phenotype                                                | gene_sfari_class | NPMI     | n_g  | n_p | n_gp |
|--------|----------------------------------------------------------|------------------|----------|------|-----|------|
| SHANK3 | ['C1853490', '22q13 Deletion Syndrome',   'MSH', 'NULL'] | 1                | 0.607088 | 1964 | 256 | 94   |
...

```

In the ‘graph_matrix_01_NPMIabove0.csv’ file, we present a matrix that shows the relationship of gene and phenotype. Its row is a gene and column is a phenotype. If the NPMI of this gene-phenotype pair is above 0, then the crosspoint would be 1. else, the crosspoint would be 0. The format should be as follows:

```
|         | ['C1535926', 'Child Mental Disorders', 'MSH', 'NULL'] | ['C0038271', 'Repetitive movements', 'HPO','HP:0000733'] | ['C0019247', 'Genetic Diseases', 'MSH','NULL'] |   |   |   |
|---------|-------------------------------------------------------|----------------------------------------------------------|------------------------------------------------|---|---|---|
| SCN2A   | 1                                                     | 0                                                        | 1                                              |   |   |   |
| CACNA1C | 1                                                     | 1                                                        | 1                                              |   |   |   |
| AFF2    | 1                                                     | 0                                                        | 1                                              |   |   |   |
|         |                                                       |                                                          |                   

```

 ### Step3: 'extract_one_gene_information.ipynb'.
 
 In the third step, we can extract one certain gene’s information using this script.
 
 You can get the README file [here](https://github.com/maiziezhoulab/Autism_GenePheno/blob/master/analysis/Step3_README.md).


