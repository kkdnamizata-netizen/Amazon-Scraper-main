 Amazon.fr High-Tech Scraper

 1. Description

Ce projet récupère automatiquement des produits de la catégorie High-Tech d'Amazon.fr en respectant une architecture MVC (Modèle - Vue - Contrôleur) orientée objet (POO) et les règles du web scraping.

Pour chaque produit, le programme extrait :
- le nom (titre)
- le prix (texte et valeur numérique pour les statistiques)
- la catégorie / sous-catégorie
- la couleur (si elle existe)
- la description et les points clés (bullets)
- jusqu'à 3 images téléchargées en haute résolution
- l'identifiant Amazon (ASIN) et l'URL propre du produit

Conformément aux consignes du mini-projet :
- Pagination : parcourt au moins 3 pages (MAX_PAGES = 3).
- Politesse : applique une pause (time.sleep) entre chaque requête et utilise un User-Agent identifiable.
- Export : enregistre les résultats en CSV, en Excel (.xlsx) et génère un rapport HTML.
- Statistiques : calcule et affiche 3 statistiques dans la console et dans le rapport HTML :
  1. Moyenne des prix
  2. Maximum des prix (avec le produit correspondant)
  3. Nombre de produits par catégorie

---

 2. Prérequis

- Windows 10 / 11
- Python 3.10+ (testé avec Python 3.13)
- Visual Studio Code
- Google Chrome installé
- Une connexion internet

---

 3. Installation (étape par étape)

Toutes les commandes se tapent dans le terminal PowerShell, depuis le dossier racine du projet.

 Étape 1 : Ouvrir le dossier du projet
Dans le terminal, se placer dans le dossier du projet :
powershell
cd chemin\vers\Amazon-Scraper-main


 Étape 2 : Créer l'environnement virtuel
À exécuter une seule fois si le dossier venv n'existe pas déjà :
powershell
python -m venv venv


 Étape 3 : Activer l'environnement virtuel
À refaire à chaque nouvelle fenêtre PowerShell :
powershell
venv\Scripts\activate

(Si PowerShell bloque l'exécution du script, taper une seule fois : Set-ExecutionPolicy -Scope CurrentUser RemoteSigned puis réessayer).

 Étape 4 : Installer les bibliothèques
Avec l'environnement virtuel (venv) activé :
powershell
python -m pip install --upgrade pip
pip install -r requirements.txt

""
---

 4. Lancer le script

Depuis la racine du projet, avec (venv) actif, exécuter :

powershell
python main.py

 Ce qui se passe :
1. Chrome s'ouvre automatiquement via Selenium.
2. Le programme charge la page de recherche des ordinateurs portables sur Amazon.fr.
3. Il détecte les sous-catégories et parcourt les pages de résultats (avec pauses de politesse entre les requêtes).
4. Il extrait les informations de chaque produit avec BeautifulSoup et télécharge jusqu'à 3 images par produit.
5. Il affiche dans la console la progression ainsi que les 3 statistiques (prix moyen, prix maximum, nombre par catégorie).
6. Il sauvegarde les fichiers CSV, Excel et le rapport HTML.

---

 5. Conception et Architecture du projet

Le projet suit l'architecture MVC structurée autour du package app/ :

text
amazon_scraper/
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── scraping_controller.py    Contrôleur : orchestre le scraping, le dépôt et les vues
│   ├── models/
│   │   ├── __init__.py
│   │   ├── depot.py                  Classe DepotProduit : stocke les produits et calcule les 3 statistiques
│   │   └── produit.py                Classe Produit : structure POO d'un produit et conversion du prix
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── amazon_scraper.py         Classe AmazonScraper : téléchargement Selenium et analyse BeautifulSoup
│   └── views/
│       ├── __init__.py
│       ├── console_view.py           Classe ConsoleView : affichage console et affichage des 3 statistiques
│       └── export_view.py            Classe ExportView : sauvegarde CSV, Excel et rapport HTML
├── data/                             Dossier de données locales
├── exports/                          Fichiers CSV exportés
├── output_amazon_technologies/       Résultats détaillés par sous-catégorie (CSV, Excel, images, rapport HTML)
├── config.py                         Paramètres globaux (URLs, délais, MAX_PAGES, MAX_PRODUCTS)
├── main.py                           Point d'entrée principal du programme
├── requirements.txt                  Liste des bibliothèques Python nécessaires
└── README.md                         Documentation du projet


 Rôle des composants :
- config.py : centralise la configuration (TECH_CATEGORY_URL, MAX_PAGES = 3, MAX_PRODUCTS, DELAY_MIN, DELAY_MAX, chemins des dossiers data/, exports/, output_amazon_technologies/).
- app/models/produit.py : définit la classe Produit (URL, ASIN, titre, prix, catégorie, couleur, description, points clés, images) et nettoie le prix pour obtenir un float (prix_numerique).
- app/models/depot.py : définit la classe DepotProduit qui regroupe les produits extraits et calcule la moyenne des prix, le prix maximum et la répartition par catégorie.
- app/scraper/amazon_scraper.py : définit la classe AmazonScraper chargée d'ouvrir les pages avec Selenium (WebDriverWait), de respecter les pauses (time.sleep), d'analyser l'arbre HTML avec BeautifulSoup et de télécharger les images avec requests.
- app/views/console_view.py : affiche la progression dans le terminal ainsi que le tableau récapitulatif des 3 statistiques.
- app/views/export_view.py : génère les fichiers .csv, .xlsx et le rapport extraction_report.html.
- app/controllers/scraping_controller.py : coordonne le scraper, le dépôt de données et les vues.
- main.py : lance l'application.

---

 6. Résultats

Les résultats sont enregistrés dans :
- exports/ : fichiers CSV consolidés.
- output_amazon_technologies/ :
  - extraction_report.html (rapport complet avec durée, résumé, 3 statistiques et erreurs éventuelles)
  - <nom de la sous-catégorie>/
    - <nom>.csv
    - <nom>.xlsx
    - images/ (images téléchargées au format ASIN_1.jpg, ASIN_2.jpg, ASIN_3.jpg)

Pour ouvrir le rapport HTML depuis PowerShell :
powershell
start output_amazon_technologies\extraction_report.html


---

 7. Réglages

Les réglages se trouvent dans le fichier config.py :
- HEADLESS = False : laisse la fenêtre Chrome visible pendant l'exécution (True pour le mode invisible --headless=new).
- MAX_PAGES = 3 : nombre de pages à parcourir par sous-catégorie (minimum 3 pages pour le mini-projet).
- MAX_PRODUCTS = 15 : nombre maximum de produits à extraire par sous-catégorie.
- DELAY_MIN = 1.5 et DELAY_MAX = 3.0 : pauses aléatoires en secondes entre les requêtes pour respecter le serveur.

---

 8. Technologies utilisées

- selenium & webdriver-manager : pilotage du navigateur Chrome pour les pages dynamiques (JavaScript).
- beautifulsoup4 & lxml : analyse de l'arbre HTML et extraction par sélecteurs CSS.
- requests : téléchargement des images produits.
- pandas & openpyxl : structuration des données et export aux formats CSV et Excel.
