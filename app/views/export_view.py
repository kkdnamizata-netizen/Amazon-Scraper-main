import json
import os
import time
import pandas as pd
from config import DATA_DIR, EXPORTS_DIR


class ExportView:
    @staticmethod
    def enregistrer_csv(produits, dossier_sortie, nom_categorie):
        if len(produits) == 0:
            return

        os.makedirs(dossier_sortie, exist_ok=True)
        os.makedirs(EXPORTS_DIR, exist_ok=True)

        donnees = [p.to_dict() for p in produits]
        df = pd.DataFrame(donnees)

        chemin_csv = os.path.join(dossier_sortie, f"{nom_categorie}.csv")
        chemin_excel = os.path.join(dossier_sortie, f"{nom_categorie}.xlsx")

        df.to_csv(chemin_csv, index=False, encoding="utf-8-sig")
        df.to_excel(chemin_excel, index=False)

        chemin_export = os.path.join(EXPORTS_DIR, f"{nom_categorie}.csv")
        df.to_csv(chemin_export, index=False, encoding="utf-8-sig")

        print(f"Fichier CSV enregistré : {chemin_csv}")

    @staticmethod
    def enregistrer_global(produits):
        if len(produits) == 0:
            return

        os.makedirs(EXPORTS_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)

        donnees = [p.to_dict() for p in produits]
        df = pd.DataFrame(donnees)

        for nom_fichier in ("produits_amazon", "tous_les_produits"):
            df.to_csv(os.path.join(EXPORTS_DIR, f"{nom_fichier}.csv"), index=False, encoding="utf-8-sig")
            df.to_excel(os.path.join(EXPORTS_DIR, f"{nom_fichier}.xlsx"), index=False)

        chemin_json = os.path.join(DATA_DIR, "produits.json")
        with open(chemin_json, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

    @staticmethod
    def generer_rapport_html(dossier_base, resume, erreurs, debut, fin, depot):
        os.makedirs(dossier_base, exist_ok=True)
        os.makedirs(EXPORTS_DIR, exist_ok=True)
        chemin_rapport = os.path.join(dossier_base, "extraction_report.html")
        chemin_rapport_exports = os.path.join(EXPORTS_DIR, "extraction_report.html")
        duree = fin - debut

        moyenne = depot.calculer_moyenne()
        max_prix, nom_max = depot.calculer_maximum()
        par_categorie = depot.compter_par_categorie()

        html = "<html><head><meta charset='utf-8'><title>Rapport Extraction</title></head><body>\n"
        html += "<h1>Rapport d'extraction Amazon.fr High-Tech</h1>\n"
        html += f"<p>Début : {time.ctime(debut)}<br>Fin : {time.ctime(fin)}<br>Durée : {duree:.2f} sec</p>\n"

        html += "<h2>Résumé</h2><ul>\n"
        for cle, valeur in resume.items():
            html += f"<li>{cle} : {valeur}</li>\n"
        html += "</ul>\n"

        html += "<h2>Statistiques (Mini-Projet)</h2><ul>\n"
        html += f"<li><strong>Moyenne des prix :</strong> {moyenne} €</li>\n"
        html += f"<li><strong>Prix maximum :</strong> {max_prix} € ({nom_max})</li>\n"
        html += "<li><strong>Nombre par catégorie :</strong><ul>\n"
        for cat, nb in par_categorie.items():
            html += f"<li>{cat} : {nb} produit(s)</li>\n"
        html += "</ul></li></ul>\n"

        html += "<h2>Erreurs</h2>\n"
        if len(erreurs) > 0:
            html += "<ul>\n"
            for err in erreurs:
                html += f"<li>{err}</li>\n"
            html += "</ul>\n"
        else:
            html += "<p>Aucune erreur.</p>\n"

        html += "</body></html>"

        for chemin in (chemin_rapport, chemin_rapport_exports):
            with open(chemin, "w", encoding="utf-8") as f:
                f.write(html)

        print(f"Rapport HTML généré : {chemin_rapport}")
