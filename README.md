## Supp_Scraper

Extreu informació de cada producte de suplementació de cada una de les 17 categories de suplements que es troben a la pàgina web https://supplementdatabase.com

Aquest paquet està format per 5 arxius:
- `requeriments.txt`: conté la informació sobre les llibreries necessàries per poder executar l'script
- `main.py`: que és l'arxiu principal que s'ha d'executar. S'ha de tenir en compte que el temps d'execució és molt llarg i per això s'ha modificat aquest arxiu per extreure només una mostra del dataset per cadascuna de les 17 categories de tipus de suplement.
- `supp_scraper.py`: és l'arxiu que conté totes les funcions per tal de poder realitzar correctament el Web Scraping.
- `supl_data.csv`: conté totes les dades extretes per les 17 categories de tipus de suplement amb un valor màxim de productes per categoria de 500 productes.
- `protein_supl_data.csv`: conté només les dades filtrades per la categoria "Protein Supplement".

## Com executar el codi
Es pot crear un nou entorn virtual executant:
````
virtualenv venv
````

S'han d'instal·lar primer els moduls necessaris que apareixen a l'arxiu `requeriments.txt`:
```
pip install -r requirements.txt
```

L'script `main.py` s'ha d'executar amb la instrucció:
```
python3 main.py 1
```

S'ha de tenir en compte que el número especificat en l'execució de l'arxiu `main.py` indica el nombre màxim de productes que es volen extreure per cada categoria de suplement. En el suposat cas que es vulgui extreure un major nombre, només cal modificar el número pel valor d'interés.

## Membres de l'equip
L'activitat ha estat realitzada conjuntament per **Anna Corral Galeote** i **Estrella Fernández Pinto**.