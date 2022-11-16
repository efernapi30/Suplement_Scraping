## Supp_Scraper

Extreu informació de cada producte de suplementació de cada una de les 17 categories de suplements que es troben a la pàgina web https://supplementdatabase.com

Aquest paquet està format per 4 arxius:
- `requeriments.txt`: conté la informació sobre les llibreries necessàries per poder executar l'script
- `main.py`: que és l'arxiu principal que s'ha d'executar. S'ha de tenir en compte que el temps d'execució és molt llarg i per això s'ha modificat aquest arxiu per extreure només una mostra del dataset, concretament 3 productes per cadascuna de les 17 categories de tipus de suplement.
- `supl_data.csv`: conté totes les dades extretes per les 17 categories de tipus de suplement amb un valor màxim de productes per categoria de 500 productes.
- `protein_supl_data.csv`: conté només les dades filtrades per la categoria "Protein Supplement".

## Com executar el codi
S'han d'instal·lar primer els moduls necessaris que apareixen a l'arxiu `requeriments.txt`:
```
pip install -r requirements.txt
```

L'script `main.py` s'ha d'executar amb la instrucció:
```
python3 main.py
```

S'ha de tenir en compte que si es volen extreure més dades de suplements, s'haurà d'accedir al document `main.py` i modificar els valors de `n_categories` i `max_prods`.

## Membres de l'equip
L'activitat ha estat realitzada conjuntament per **Anna Corral Galeote** i **Estrella Fernández Pinto**.