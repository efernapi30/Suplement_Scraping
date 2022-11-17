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

def get_page(user_agent: str):
    page_all = requests.get('https://supplementdatabase.com/supp-products.php', headers=user_agent)
    soup_all = BeautifulSoup(page_all.content, 'html.parser') # Parsing content using beautifulsoup
    return soup_all

def get_list_supl_links(user_agent: str):
    list_supl_links = []
    soup_all = get_page(user_agent)
    all_supl_prod = soup_all.find("aside", class_="sidebar pb-4")
    all_supl_prod = all_supl_prod.select("aside div a")

    for ref in all_supl_prod:
        word = "supplement-product-filter"
        if word in ref["href"]:
            list_supl_links.append(ref["href"])
    
    return list_supl_links

def sacraper_supl_data(user_agent: str, list_supl_links: list, n_categories: tuple, max_prods: int):
    start = datetime.now()
    n_rows = 0
    data = []

    # Passem per cada un dels links de cada categoria de tipus de suplement
    for type in list_supl_links[n_categories[0]:n_categories[1]]:
        try:
            page = requests.get(type, headers=user_agent, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Creem una llista amb tots els productes pel tipus de suplement
            all_products = soup.select("table tbody tr td a")
            list_prod_links = []
            max_val = 1

            for product in all_products:
                if max_val <= max_prods:
                    page_link = "https://supplementdatabase.com/" + product["href"]
                    list_prod_links.append(page_link)
                    max_val = max_val + 1
        except requests.exceptions.Timeout:
            pass

        # Entrem a cada un dels links dels productes de la llista per obtenir la informació d'interès
        for link in list_prod_links:
            row = {}
            try:
                prod_page = requests.get(link, headers=user_agent, timeout=10)
                prod_soup = BeautifulSoup(prod_page.content, 'html.parser')
                
                # Get list of elements
                elements = prod_soup.find("ul", class_="list list-icons list-icons-sm")
                for ele in elements:
                    text = ele.get_text()
                    if len(text) > 1:
                        key, value = text.split(": ", 1)
                        if key == "Manufacturer Website":
                            r = ele.find("a")["href"]
                            row[key] = r
                        elif key == "Manufacturer Social Media":
                            r = ele.find("a")["href"]
                            row[key] = r
                        elif key == "Research Rating":
                            r = re.search("(.*)\(above 60 indicates sufficient research\)", value).groups()
                            row[key] = r[0]
                        elif key == "Serving Size":
                            if "(" in value:
                                r = re.search("\w+\s\w+ \((.*)\)", value).groups()
                                row[key] = r[0]
                            else:
                                row[key] = value
                        elif key == "Calories per Serving":
                            r = re.search("(.*) calories", value).groups()
                            row[key] = r[0]
                        elif "Ranking within" in key:
                            if key == "Ranking within all Supplement Products":
                                row[key] = value
                            else:
                                row["Ranking within Supplement Category"] = value
                        else:
                            row[key] = value

                # Get Updated date
                updated_date = prod_soup.find("i", class_="fas fa-clock").next_element
                updated_date = re.search("Updated (.*), (.*)", updated_date).groups()
                row["Updated Month Day"] = updated_date[0]
                row["Updated Year"] = updated_date[1]

                # Protein Sup. only
                if row["Supplement Category"] == "Protein Supplements":
                    # Get Macros percentage in Protein Sup.
                    info = prod_soup.find("div", class_="col-lg-9")
                    for i in info: 
                        i = str(i)
                        if "<li>fat" in i:
                            fat = re.search("<li>fat: (.*)%</li>", i).groups()
                            carbs = re.search("<li>carbohydrates: (.*)%</li>", i).groups()
                            prot = re.search("<li>protein: (.*)%</li>", i).groups()
                            row.update({"Fat (%)": fat[0], "Carbohydrates (%)": carbs[0], "Protein (%)": prot[0]})

                    # Get Macros information in Protein Sup.
                    macros_info = str(prod_soup.find("a", id="macros").next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element)
                    macros_info = re.search("<p>(.*)</p>", macros_info).groups()
                    row["Macros details"] = macros_info[0]

                # Afegim cada fila d'informació extreta a la llista "data"
                data.append(row)

                # Anem visualitzant cada link executat, el temps de resposta total i el nombre de links als qual s'han accedit
                n_rows = n_rows+1
                add_one_row = datetime.now()
                resp_delay = str(add_one_row-start)
                print("Web page: " + link)
                print("Response delay: " + resp_delay)
                print("Number of links scraped: " + str(n_rows))

            except requests.exceptions.Timeout:
                pass

            except requests.exceptions.RequestException:
                pass
    return data

def convert_data_list_to_df(data):
    df_all_supl_prod = pd.DataFrame(data)
    message = "List transformed to DataFrame successfully!"
    print(message)
    return df_all_supl_prod

def filter_SupCategory_name(df_all_supl_prod: pd.DataFrame, supl_name: str):
    df_protein_supl_prod = df_all_supl_prod[df_all_supl_prod["Supplement Category"] == supl_name]
    return df_protein_supl_prod

def export_df_to_csv(df: pd.DataFrame, name_csv: str):
    df.to_csv(name_csv+".csv", index=False)
    message = "File '" + name_csv + ".csv' created successfully!"
    print(message)
    return
