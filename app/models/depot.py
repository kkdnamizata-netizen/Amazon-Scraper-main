class DepotProduit:
    def __init__(self):
        self.produits = []

    def ajouter(self, produit):
        if produit is not None:
            self.produits.append(produit)

    def calculer_moyenne(self):
        total = 0.0
        compteur = 0

        for p in self.produits:
            prix = p.obtenir_prix_nombre()
            if prix > 0:
                total = total + prix
                compteur = compteur + 1

        if compteur == 0:
            return 0.0

        return round(total / compteur, 2)

    def calculer_maximum(self):
        max_prix = 0.0
        nom_produit = "Aucun"

        for p in self.produits:
            prix = p.obtenir_prix_nombre()
            if prix > max_prix:
                max_prix = prix
                nom_produit = p.title

        return max_prix, nom_produit

    def compter_par_categorie(self):
        categories = {}

        for p in self.produits:
            cat = p.categorie
            if cat in categories:
                categories[cat] = categories[cat] + 1
            else:
                categories[cat] = 1

        return categories
