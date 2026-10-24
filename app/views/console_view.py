class ConsoleView:
    @staticmethod
    def afficher_debut():
        print("==================================================")
        print("   DEMARRAGE DU SCRAPER AMAZON (MINI-PROJET POO)  ")
        print("==================================================")

    @staticmethod
    def afficher_message(texte):
        print(texte)

    @staticmethod
    def afficher_produit(numero, produit):
        print(f"[{numero}] {produit.title[:60]}... - Prix : {produit.price}")

    @staticmethod
    def afficher_statistiques(depot):
        moyenne = depot.calculer_moyenne()
        max_prix, nom_max = depot.calculer_maximum()
        par_categorie = depot.compter_par_categorie()

        print("\n==================================================")
        print("   LES 3 STATISTIQUES DU MINI-PROJET")
        print("==================================================")
        print(f"1. Moyenne des prix        : {moyenne} €")
        print(f"2. Prix maximum            : {max_prix} € ({nom_max[:40]}...)")
        print("3. Nombre par catégorie    :")
        for categorie, nombre in par_categorie.items():
            print(f"   - {categorie} : {nombre} produit(s)")
        print("==================================================\n")
