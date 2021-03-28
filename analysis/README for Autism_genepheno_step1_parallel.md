Run 'Autism_genepheno_step1_parallel.py' to speed up using a parallel method of Python and get the target results of step1. 
 
 ```
python Autism_genepheno_step1_parallel.py --ASDPTO_dir ./source/ASDPTO.csv --UMLS_dir ./source/UMLS.txt --allGene_dir ./source/VariCarta_Autism_gene.tsv --papers_dir ./XML_Autism_datasets_5years/ --HPOtreeview_dir ./HPO_treeview.txt --out_dir ./Autism_genepheno_results/
```
#### *Parameters
##### --ASDPTO_dir, default = './source/ASDPTO.csv'
##### --UMLS_dir, default = './source/UMLS.txt'
##### --allGene_dir, default = './source/VariCarta_Autism_gene.tsv'
##### --papers_dir, default = './XML_Autism_datasets_5years/'
##### --HPOtreeview_dir, default = './HPO_treeview.txt'
##### --out_dir, default = './Autism_genepheno_results/'

#### Note that the default directories are the same as those in 'Autism_genepheno_step1.ipynb'.
