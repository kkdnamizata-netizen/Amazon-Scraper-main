import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, HEADLESS, USER_AGENT, WAIT_TIMEOUT, PAUSE_SECONDES
from app.models.produit import Produit


class AmazonScraper:
    def __init__(self):
        self.pilote = None
        self.erreurs = []
        self.images_telechargees = 0

    def ouvrir_navigateur(self):
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument(f"--user-agent={USER_AGENT}")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.pilote = webdriver.Chrome(options=options)
        return self.pilote

    def fermer_navigateur(self):
        if self.pilote:
            try:
                self.pilote.quit()
            except Exception:
                pass
            self.pilote = None

    def telecharger_page(self, url):
        try:
            self.pilote.get(url)
            WebDriverWait(self.pilote, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(PAUSE_SECONDES)
            return True
        except Exception as e:
            self.erreurs.append(f"Erreur sur {url} : {e}")
            return False

    def trouver_sous_categories(self, url_depart):
        if not self.telecharger_page(url_depart):
            return []

        soup = BeautifulSoup(self.pilote.page_source, "html.parser")
        sous_categories = []
        noms_vus = set()

        liens = soup.select("a[href*='/s?']")
        for lien in liens:
            href = lien.get("href")
            nom = lien.get_text(strip=True)

            if href and nom and "ordinateur" in nom.lower() and nom.lower() not in noms_vus:
                if not href.startswith("http"):
                    url_complete = BASE_URL.rstrip("/") + href
                else:
                    url_complete = href
                noms_vus.add(nom.lower())
                sous_categories.append((nom, url_complete))

        if len(sous_categories) == 0:
            sous_categories.append(("Ordinateurs portables", url_depart))

        return sous_categories

    def extraire_liens_produits(self):
        soup = BeautifulSoup(self.pilote.page_source, "html.parser")
        liens_propres = []

        for balise in soup.select("a[href*='/dp/']"):
            href = balise.get("href")
            if href and "/dp/" in href:
                parties = href.split("/dp/")
                if len(parties) > 1:
                    asin = parties[1][:10]
                    url_produit = f"https://www.amazon.fr/dp/{asin}"
                    if url_produit not in liens_propres:
                        liens_propres.append(url_produit)

        lien_suivant = None
        bouton_suivant = soup.select_one("a.s-pagination-next")
        if bouton_suivant and bouton_suivant.get("href"):
            href_suivant = bouton_suivant.get("href")
            if href_suivant.startswith("http"):
                lien_suivant = href_suivant
            else:
                lien_suivant = BASE_URL.rstrip("/") + href_suivant

        return liens_propres, lien_suivant

    def extraire_produit(self, url, dossier_sortie, categorie):
        if not self.telecharger_page(url):
            return None

        soup = BeautifulSoup(self.pilote.page_source, "html.parser")

        asin = url.split("/dp/")[1][:10] if "/dp/" in url else "INCONNU"

        element_titre = soup.select_one("#productTitle")
        titre = element_titre.get_text(strip=True) if element_titre else "Sans titre"

        element_prix = soup.select_one(".a-price .a-offscreen")
        prix = element_prix.get_text(strip=True) if element_prix else None

        element_label = soup.select_one("#acBadge_feature_div .ac-badge-text-primary, .p13n-best-seller-badge")
        label = element_label.get_text(" ", strip=True) if element_label else None

        element_couleur = soup.select_one("#variation_color_name .selection, #inline-twister-expanded-dimension-text-color_name")
        couleur = element_couleur.get_text(strip=True) if element_couleur else None

        bullets = []
        for li in soup.select("#feature-bullets li"):
            texte = li.get_text(strip=True)
            if texte:
                bullets.append(texte)

        element_desc = soup.select_one("#productDescription")
        if element_desc:
            description = element_desc.get_text(" ", strip=True)
        else:
            description = " ".join(bullets)

        images = []
        for img in soup.select("#altImages img, #landingImage"):
            src = img.get("src")
            if src and "/images/I/" in src and src not in images:
                images.append(src)

        dossier_images = os.path.join(dossier_sortie, "images")
        os.makedirs(dossier_images, exist_ok=True)

        for i, img_url in enumerate(images[:3]):
            try:
                reponse = requests.get(img_url, timeout=10)
                if reponse.status_code == 200:
                    chemin_image = os.path.join(dossier_images, f"{asin}_{i + 1}.jpg")
                    with open(chemin_image, "wb") as f:
                        f.write(reponse.content)
                    self.images_telechargees += 1
            except Exception as e:
                self.erreurs.append(f"Erreur image {img_url} : {e}")

        return Produit(
            url=url,
            asin=asin,
            title=titre,
            price=prix,
            categorie=categorie,
            color=couleur,
            description=description,
            bullets=bullets,
            images=images,
            label=label
        )
