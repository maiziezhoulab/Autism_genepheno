Create three folders named 'Extraced_results', 'Sum_for_each_paper' and 'Sum_all' in the directory to save the results.

Go through the jupyter cells one by one. The final cell will run the function which starts to output the results at the beginning or at where you stopped last time.

Note that there are bunches of input files in the functions.
They are 'ASDPTO.csv' in the folder 'Phenotype_list', which saves the ASDPTO part phenotype list;
              'UMLS.txt' in the folder 'Phenotype_list', which saves the UMLS part phenotype list;
              'del_ls_HPOtreeview.txt' in the folder 'Phenotype_list', which saves the upper-level concepts of HPO list which are supposed to be removed;
              'HPO(treeview).txt' in the folder 'Phenotype_list', which saves the treeview form of HPO list;
              'c2upper.txt' in the folder 'Phenotype_list', which saves the phenotypes and their respective upper level concepts;
              'export_latest.tsv' in the folder 'Genotype_list', which saves the genotype list;
              'XML_datasets_5year' folder, which saves our target papers in the last five years.
Please make sure they are in the same format as ours if you want to use your own input files or change their respective reading directories if you want to put the input files arbitrarily.

Outputs will be presented in 'Extraced_results' folder, which saves the extracted sentences/genotypes/phenotypes for each paper as:
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
        }, 
...;
'Sum_for_each_paper' folder, which saves n_g (occured genotypes and the times they occured) and n_p (occured phenotypes and the times they occured) for each paper;
and 'Sum_all' folder, which saves the overall summary (number of paper processed, number of sentences extracted, unique genotypes, overall n_g and n_p, etc) of our work. 