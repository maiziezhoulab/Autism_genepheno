 ### Step3: 'extract_one_gene_information.ipynb'.
 
In the third step, we can extract one certain gene’s information using this script. 

The dir of the input file and output file is shown in the second cell of the script.

```
#define dir

# input dir
json_path = '.\\Extraced_results'             # the output file of step1
np_dir = '.\\Sum_all\\n_p.txt'                # the output file of step1
ng_dir = '.\\Sum_all\\n_g.txt'                # the output file of step1
In_Summary_dir='.\\Sum_all\\In_Summary.txt'   # the output file of step1
NPMI_dir='.\\NPMI_file\\NPMI.json'            # the output file of step2

# output dir
one_information_dir = '.\\one_gene_information\\'
```

The certain gene is defined in the third cell of the script.

```
# define the extracted gene
gene_extract = "SLC38A11"
```

When finished, you will get:
```
|-one_gene_information
    |-xxx_information.json
    |-xxx_summary.txt
```


In the ‘xxx_information.json’ file, the information of a certain gene is given. The format should be as follows:

```
{
    "Gene name": "SHANK3",
    "Gene sfari class": 1.0,
    "Related phenotype NPMI": {
        "['ASDPTO', 'Language Development', 'ASDPTO', 'NULL']": 0.1373911873070885,
        "['ASDPTO', 'Tuberous Sclerosis', 'ASDPTO', 'NULL']": 0.1926806997306739,
        ...
    }, "Related sentences": {
        "Sentence001": {
            "Content": "In contrast to contiguous gene syndromes such as Williams syndrome, several other microdeletion syndromes have been shown recently to be caused mainly by haploinsufficiency of a single responsible gene such as MEF2C in 5q14.3 microdeletion syndrome [24] or SHANK3 in Phelan-McDermid syndrome [25].",
            "Gene": [
                "MEF2C",
                "SHANK3"
            ],
            "Normolized phenotype": [
                [
                    "C1853490",
                    "22q13 Deletion Syndrome",
                    "MSH",
                    "NULL"
                ],
                [
                    "C0175702",
                    "Beuren Syndrome",
                    "MSH",
                    "NULL"
                ],
                [
                    "C4304529",
                    "5q14.3 microdeletion syndrome",
                    "SNOMEDCT_US",
                    "NULL"
                ]
            ],
            "Original phenotype": [
                "Phelan-McDermid syndrome",
                "Williams syndrome",
                "5q14 3 microdeletion syndrome"
            ],
            "PMCid": "PMC4587785",
            "Title": "Microdeletions in 9q33.3-q34.11 in five patients with intellectual disability, microcephaly, and seizures of incomplete penetrance: is STXBP1 not the only causative gene? (Published on 9/29/2015)",
            "Upper level concepts (HPO only)": []
        },
        ......
    },
    "Summary": {
        "Normolized phenotype number": 167,
        "Paper list": [
            "PMC6995976",
            "PMC6018399",
            "PMC5677962",
            ...
        ],
       
      "Paper name list": [
          "Severe white matter damage in SHANK3 deficiency: a human and translational study (Published on 12/02/2019) [Only abstract]",
          "Dissecting the Genetics of Autism Spectrum Disorders: A Drosophila Perspective (Published on 8/07/2019)",
          "GABA Neuronal Deletion of Shank3 Exons 14\u201316 in Mice Suppresses Striatal Excitatory Synaptic Input and Induces Social and Locomotor Abnormalities (Published on 10/09/2018)",
          ......
        ],
        "Paper number": 179,
        "Sentence number": 344
    }
}
```

In the ‘xxx_summary.txt’, the summary in the ‘xxx_information.json’ file is given.
