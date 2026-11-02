class Produit:
    def __init__(self, url, asin, title, price, categorie="Non classé", color=None, description=None, bullets=None, images=None, label=None):
        self.url = url
        self.asin = asin
        self.title = title
        self.price = price
        self.categorie = categorie
        self.label = label
        self.color = color
        self.description = description
        self.bullets = bullets if bullets else []
        self.images = images if images else []
        self.prix_numerique = self.obtenir_prix_nombre()

    def obtenir_prix_nombre(self):
        if not self.price:
            return 0.0

        texte = str(self.price)
        texte = texte.replace("€", "").replace(" ", "").replace("\xa0", "").replace("\u202f", "")
        texte = texte.replace(",", ".")

        try:
            return float(texte)
        except ValueError:
            return 0.0

    def to_dict(self):
        texte_bullets = "; ".join(self.bullets) if self.bullets else ""
        return {
            "url": self.url,
            "asin": self.asin,
            "title": self.title,
            "price": self.price,
            "prix_numerique": self.obtenir_prix_nombre(),
            "categorie": self.categorie,
            "label": self.label,
            "color": self.color,
            "description": self.description,
            "bullets": texte_bullets,
            "images_count": len(self.images)
        }
