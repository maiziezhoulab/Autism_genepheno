"""
a scraper for collecting xml format paper in PMC
link: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id= + serial # of paper(PMC id)
"""
#!/usr/bin/env python
import pdb
#pdb.set_trace()
import requests
from bs4 import BeautifulSoup
import os
import time
import sys
from argparse import ArgumentParser
# import urllib.request as rqst
parser = ArgumentParser(description="download all papers in XML format from PMC website",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--pmc_id_list','-pmc',help="Required parameter; a txt file to store papers' PMCID, one PMCID per line",required=True)
parser.add_argument('--time_elapsed','-t',type=int,help="wait some time to download another batch of 300 papers", default=1800)
parser.add_argument('--num_threads_spades','-t_spades',type=int,help="number of threads for spades, default = 5", default=5)
parser.add_argument('--out_dir','-o', help="Directory to store output results, default = ./XML_datasets",default="./XML_datasets")
args = parser.parse_args()


def ncbi_pubmed_pmcId_scraper(pmc_id_file_path, out_dir, time_elapsed):
    """
    scraping xml format papers based on PMC ids

    :param xml_file_link: ncbi pubmed xml format bulky downloading API
    :param pmc_id_file_path: path to file of PMC ids
    :param out_dir: relative out directory to save .xml files
    :param time_elapsed: time to sleep every 300 iterations
    :return: None
    """
    # xml_file_link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="
    # time_elapsed = 3600
    # pmc_id_file_path = 'pmc_result.txt'
    # out_dir = 'XML_datasets'
    xml_file_link="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="
    with open(pmc_id_file_path, "r") as file:
        ids = file.readlines()
        ids = [item.replace('PMC','') for item in ids]
        ids = [item.replace('\n','') for item in ids]
    # print(lines)
    # exit(-1)
    downloaded_files = []
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        downloaded_files = os.listdir(out_dir)
        print("downloaded files:")
        #print(downloaded_files)


    # exit(-1)
    count = 0
    for id_ in ids:
        link = xml_file_link + id_.strip().split("C")[0]

        if id_.strip() + ".xml" in downloaded_files:
            print("already downloaded")
            continue
        print(link)
        # exit(-1)
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(str(soup))
        # exit(-1)
        file_name = id_.strip() + ".xml"
        with open(os.path.join(out_dir, file_name), "w", encoding='utf-8') as file:
            file.write(str(soup))
        count += 1
        if count % 300 == 0:
            time.sleep(time_elapsed)
        # exit(-1)


def ncbi_pubmed_pmcId_scraper_pdf(pdf_file_link="https://www.ncbi.nlm.nih.gov/pmc/articles/",
                                  pmc_id_file_path="pmc_result.txt", out_dir='PDF_paper', time_elapsed=3600):
    """
    scraping xml format papers based on PMC ids

    :param pdf_file_link: ncbi pubmed xml format bulky downloading API
    :param pmc_id_file_path: path to file of PMC ids
    :param out_dir: relative out directory to save .xml files
    :param time_elapsed: time to sleep every 300 iterations
    :return: None
    """
    # xml_file_link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="
    # time_elapsed = 3600
    # pmc_id_file_path = 'pmc_result.txt'
    # out_dir = 'XML_paper'
    with open(pmc_id_file_path, "r") as file:
        ids = file.readlines()

    # print(lines)
    # exit(-1)
    downloaded_files = []
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        downloaded_files = os.listdir(out_dir)
        print("downloaded files:")
        print(downloaded_files)

    # exit(-1)
    count = 0
    for id_ in ids:
        link = pdf_file_link + id_.strip() + '/'

        if id_.strip() + ".pdf" in downloaded_files:
            print("already downloaded")
            continue
        print(link)
        # exit(-1)
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.find_all('link')
        for lks in links:
            href = lks['href']
            if href.endswith('.pdf'):
                url = link + 'pdf' + '/' + href.split('/')[-1]
                print(url)
                download_file(url, os.path.join(out_dir, id_.strip() + ".pdf"))
                break

        # exit(-1)
        # print(str(soup))
        # exit(-1)
        # file_name = id_.strip() + ".xml"
        # with open(os.path.join(out_dir, file_name), "w", encoding='utf-8') as file:
        #     file.write(str(soup))
        count += 1
        if count % 300 == 0:
            time.sleep(time_elapsed)


def download_file(download_url, save_dir):
    # response = rqst.urlopen(download_url)
    # file = open(file_name, 'wb')
    # file.write(response.read())
    # file.close()
    r = requests.get(download_url)
    with open(save_dir, 'wb') as outfile:
        outfile.write(r.content)
    print("Completed")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        Popen("python3 " + "Autism_genepheno_PMC_scraper.py -h",shell=True).wait()
    else:
        pmc_id_list = args.pmc_id_list
        time_elapsed = args.time_elapsed
        out_dir = args.out_dir
        if os.path.exists(out_dir):
            print("using existing output folder: " + out_dir)
        else:
            os.makedirs(out_dir)
        ncbi_pubmed_pmcId_scraper(pmc_id_file_path=pmc_id_list,out_dir=out_dir,time_elapsed = time_elapsed)

