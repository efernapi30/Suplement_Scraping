from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd
import time
from datetime import datetime
import whois
import builtwith
import supp_scraper


if __name__ == "__main__":

# Definim les variables que necessitarem introduir a cada funció
	user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'}
	n_categories = (0, 17)
	max_prods = 2
	supl_name = "Protein Supplements"
	name_csv_all_supl_prod = "supl_data"
	name_csv_protein_supl_prod = "protein_supl_data"

	list_supl_links = supp_scraper.get_list_supl_links(user_agent)
	data = supp_scraper.sacraper_supl_data(user_agent, list_supl_links, n_categories, max_prods)

# Agafem la llista amb les dades i la transformem a un DataFrame
	df_all_supl_prod = supp_scraper.convert_data_list_to_df(data)

# Filtrem la llista per la categoria del tipus de suplement que ens interessa
	df_protein_supl_prod = supp_scraper.filter_SupCategory_name(df_all_supl_prod, supl_name)

# Exportem el dataset creat a un arxiu .csv
	supp_scraper.export_df_to_csv(df_all_supl_prod, name_csv_all_supl_prod)
	supp_scraper.export_df_to_csv(df_protein_supl_prod, name_csv_protein_supl_prod)
