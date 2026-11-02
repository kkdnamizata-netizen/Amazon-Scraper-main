import os
import time
from config import TECH_CATEGORY_URL, OUTPUT_DIR, MAX_PAGES, MAX_PRODUCTS
from app.models.depot import DepotProduit
from app.scraper.amazon_scraper import AmazonScraper
from app.views.console_view import ConsoleView
from app.views.export_view import ExportView


class ScrapingController:
    def __init__(self):
        self.depot = DepotProduit()
        self.scraper = AmazonScraper()
        self.resume = {
            "subcategories_processed": 0,
            "products_extracted": 0,
            "images_downloaded": 0,
            "pages_scraped": 0
        }

    def scraper_categorie(self, nom_categorie, url_depart):
        nom_propre = ""
        for c in nom_categorie:
            if c.isalnum() or c in " _-":
                nom_propre += c
        nom_propre = nom_propre[:60]

        sous_dossier = os.path.join(OUTPUT_DIR, nom_propre)
        os.makedirs(sous_dossier, exist_ok=True)

        produits_categorie = []
        url_page = url_depart
        numero_page = 0

        while url_page and numero_page < MAX_PAGES and len(produits_categorie) < MAX_PRODUCTS:
            numero_page += 1
            ConsoleView.afficher_message(f"\n--- Page {numero_page} : {url_page} ---")

            if not self.scraper.telecharger_page(url_page):
                break

            self.resume["pages_scraped"] += 1

            liens, lien_suivant = self.scraper.extraire_liens_produits()
            ConsoleView.afficher_message(f"{len(liens)} liens produits trouvés")

            for lien in liens:
                if len(produits_categorie) >= MAX_PRODUCTS:
                    break

                produit = self.scraper.extraire_produit(lien, sous_dossier, nom_categorie)
                if produit:
                    produits_categorie.append(produit)
                    self.depot.ajouter(produit)
                    self.resume["products_extracted"] += 1
                    ConsoleView.afficher_produit(len(produits_categorie), produit)

            url_page = lien_suivant

        self.resume["images_downloaded"] = self.scraper.images_telechargees
        self.resume["subcategories_processed"] += 1

        ExportView.enregistrer_csv(produits_categorie, sous_dossier, nom_propre)

    def lancer(self):
        ConsoleView.afficher_debut()
        debut = time.time()

        try:
            self.scraper.ouvrir_navigateur()

            sous_categories = self.scraper.trouver_sous_categories(TECH_CATEGORY_URL)
            ConsoleView.afficher_message(f"Trouvé {len(sous_categories)} sous-catégorie(s).")

            for nom, lien in sous_categories[:1]:
                ConsoleView.afficher_message(f"\nScraping de la sous-catégorie : {nom}")
                self.scraper_categorie(nom, lien)
        finally:
            self.scraper.fermer_navigateur()

        fin = time.time()

        ConsoleView.afficher_statistiques(self.depot)

        ExportView.enregistrer_global(self.depot.produits)
        ExportView.generer_rapport_html(
            OUTPUT_DIR,
            self.resume,
            self.scraper.erreurs,
            debut,
            fin,
            self.depot
        )

        ConsoleView.afficher_message("\nScraping terminé avec succès !")
