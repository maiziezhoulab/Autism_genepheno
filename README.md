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

 ### Go through the cells of Jupyter Notebook 'NPMI_calculate.ipynb'.
 
The second step is analyzing the result in the first step. This script will calculate the NPMI of each pair and also output the gene-phenotype matrix. 

The dir of the input file and output file is shown in the second cell of the script.

```
# input file dir
json_path = '.\\Extraced_results'# the path of output file in 'Gene_Phenotype_Extraction.ipynb'
jsons = glob.glob("{}\\*.json".format(json_path)) # get the dir of every file in .\\Extraced_results
np_dir = '.\\Sum_all\\n_p.txt'# the output file in 'Gene_Phenotype_Extraction.ipynb'
ng_dir = '.\\Sum_all\\n_g.txt'# the output file in 'Gene_Phenotype_Extraction.ipynb'
In_Summary_dir='.\\Sum_all\\In_Summary.txt'# the output file in 'Gene_Phenotype_Extraction.ipynb'
sfari_gene_dir='.\\Genotype_list\\SFARI-Gene_genes_12-11-2020release_12-19-2020export.xlsx'# the SFARI genes file dir

genes_outlier = ['BDNF']# define gene outlier

# output file dir
NPMI_dir='.\\NPMI_file\\NPMI.json' # raw NPMI json file
NPMI_csv_dir='.\\NPMI_file\\NPMI.csv'# raw NPMI csv file
NPMI_above_zero_csv_dir='.\\NPMI_file\\NPMI_above_zero.csv'# pairs with NPMI above 0, csv file
graph_matrix_dir = '.\\NPMI_file\\graph_matrix_01_NPMIabove0.csv'# matrix, NPMI>0 -> 1,NPMI<=0 -> 0
```
About the input, apart from the output file in the first step, the SFARI genes file is needed.

Also, by defining the list ‘genes_outlier’, we can delete some genes which are known as outliers in the gene list. 

About the output, all the output file is put in ‘NPMI_file’.

In the ‘NPMI.json’ file, the gene-phenotype pairs’ NPMI, n_g, n_p, n_gp and gene_sfari_class are noted down as JSON files, named after the gene names and phenotype names. Presenting a JSON file would make it easier for further data analysis. The format should be as follows:

```
[
    {
        "gene": "CA1",
        "phenotype": "['C0027651', 'Neoplasia', 'HPO', 'HP:0002664']",
        "NPMI": -0.2549212816058176,
        "gene_sfari_class": "NA",
        "n_g": 5163,
        "n_p": 23384,
        "n_gp": 1.0
    },
    {
        "gene": "CA1",
        "phenotype": "['C0006826', 'Cancer', 'HPO', 'HP:0002664']",
        "NPMI": -0.2346279960018859,
        "gene_sfari_class": "NA",
        "n_g": 5163,
        "n_p": 29419,
        "n_gp": 2.0
    },
    ...
]
```

In the ‘NPMI.csv’ file, the same data as the ‘NPMI.json’ file is presented in a CSV file. The format should be as follows:

```
gene,phenotype,gene_sfari_class,NPMI,n_g,n_p,n_gp
GEM,"['C0346326', 'Optic glioma', 'HPO', 'HP:0009734']",NA,0.4216545678251195,156,34,1.0
GEM,"['C3665386', 'Loss of vision', 'OMIM, HPO', 'HP:0000572']",NA,0.3866853509894122,156,262,3.0
GEM,"['C0031099', 'Periodontitis', 'MSH, OMIM, SNOMEDCT_US, HPO', 'HP:0000704']",NA,0.3412615687957112,156,112,1.0
...
FAS,"['C3146244', 'Alcohol Related Birth Defects', 'MSH', 'NULL']",NA,0.7067812880215343,201,6,5.0
FAS,"['C0015923', 'FAS - Fetal alcohol syndrome', 'SNOMEDCT_US', 'NULL']",NA,0.6899769648899337,201,78,20.0
FAS,"['C3661483', 'Partial Fetal Alcohol Syndrome', 'MSH', 'NULL']",NA,0.6423665193607985,201,1,1.0
...

```
In the ‘NPMI_above_zer.csv’ file, pairs that have NPMI>0 is presented in a CSV file. These pairs are considered as strong pairs. The format should be the same as the ‘NPMI.csv’ file.

In the ‘graph_matrix_01_NPMIabove0.csv’ file, we present a matrix that shows the relationship of gene and phenotype. Its row is a gene and column is a phenotype. If the NPMI of this gene-phenotype pair is above 0, then the crosspoint would be 1. else, the crosspoint would be 0. The format should be as follows:

```
	['C1535926', 'Child Mental Disorders', 'MSH', 'NULL']	['C0038271', 'Repetitive movements', 'HPO', 'HP:0000733']	['C0019247', 'Genetic Diseases', 'MSH', 'NULL'] ...
GEM	0	0	0 ...
FAS	1	0	1 ...
UBE3A	1	1	0 ...
...

```

 ### Go through the cells of Jupyter Notebook 'extract_one_gene_information.ipynb'.
 

In the third step, we can extract one certain gene’s information using this script. 

The dir of the input file and output file is shown in the second cell of the script.

```
#define dir
json_path = '.\\Extraced_results'
jsons = glob.glob("{}\\*.json".format(json_path)) 
# input dir
NPMI_dir='.\\NPMI_file\\NPMI.json'
np_dir = '.\\Sum_all\\n_p.txt'
ng_dir = '.\\Sum_all\\n_g.txt'
In_Summary_dir='.\\Sum_all\\In_Summary.txt'
# output dir
one_information_dir = '.\\one_gene_information\\'
```
The certain gene is defined in the third cell of the script.

```
# define the extracted gene
gene_extract = "SLC38A11"
```

About the output, all the output file is put in ‘one_gene_information’.

In the ‘xxx_information.json’ file, the information of a certain gene is given. The format should be as follows:

```
{
    "Gene name": "SLC38A11",
    "Gene sfari class": "NA",
    "Related phenotype NPMI": {
        "['C0040517', \"(Psychogenic tics) or (Gilles de la Tourette's syndrome)\", 'SNOMEDCT_US', 'NULL']": 0.4482389306173313,
        "['C2169806', 'Tic disorder', 'SNOMEDCT_US, HPO', 'HP:0100033']": 0.3829211143253955
    },
    "Related sentences": {
        "Sentence001": {
            "Content": "Thus, heterozygous deletion of these genes might also play a pivotal role in conferring ASD symptoms and could even be suggested to confer symptoms of Tourette syndrome in the present case: Loss of SLC38A11, a putative sodium-coupled neutral amino acid transporter [23] might enhance the effects of SCN2A and SCN3A deletion.",
            "Gene": [
                "SLC38A11",
                "SCN2A",
                "SCN3A"
            ],
            "Normolized phenotype": [
                [
                    "C0040517",
                    "(Psychogenic tics) or (Gilles de la Tourette's syndrome)",
                    "SNOMEDCT_US",
                    "NULL"
                ]
            ],
            "Original phenotype": [
                "Tourette syndrome"
            ],
            "PMCid": "PMC6090917",
            "Title": "Heterozygous deletion of SCN2A and SCN3A in a patient with autism spectrum disorder and Tourette syndrome: a case report (Published on 8/2/2018)",
            "Upper level concepts (HPO only)": []
        },
        "Sentence002": {
            "Content": "It remains to be elucidated whether the heterozygous loss of SCN2A and SCN3A or GRB14, COBLL1 and SLC38A11, respectively, might also contribute to the development of tics, which remains subject to investigation in large hypothesis-driven association studies.",
            "Gene": [
                "SCN2A",
                "SCN3A",
                "GRB14",
                "COBLL1",
                "SLC38A11"
            ],
            "Normolized phenotype": [
                [
                    "C2169806",
                    "Tic disorder",
                    "SNOMEDCT_US, HPO",
                    "HP:0100033"
                ]
            ],
            "Original phenotype": [
                "tics"
            ],
            "PMCid": "PMC6090917",
            "Title": "Heterozygous deletion of SCN2A and SCN3A in a patient with autism spectrum disorder and Tourette syndrome: a case report (Published on 8/2/2018)",
            "Upper level concepts (HPO only)": [
                "Abnormality of the nervous system"
            ]
        }
    },
    "Summary": {
        "Normolized phenotype number": 2,
        "Paper list": [
            "PMC6090917"
        ],
        "Paper name list": [
            "Heterozygous deletion of SCN2A and SCN3A in a patient with autism spectrum disorder and Tourette syndrome: a case report (Published on 8/2/2018)"
        ],
        "Paper number": 1,
        "Sentence number": 2
    }
}
```

In the ‘xxx_summary.txt’, the summary in the ‘xxx_information.json’ file is given.

